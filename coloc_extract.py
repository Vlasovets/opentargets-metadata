import argparse
import logging
import os
from typing import Dict, List, Optional
import duckdb
import pyarrow as pa

def discover_columns(con: duckdb.DuckDBPyConnection, table_paths: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Inspect available columns from each Parquet file using DuckDB.
    Returns a dict mapping table name to list of columns.
    """
    columns = {}
    for name, path in table_paths.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"Required Parquet file missing: {path}")
        cols = con.execute(f"DESCRIBE SELECT * FROM read_parquet('{path}')").fetchdf()["column_name"].tolist()
        columns[name] = cols
    return columns

def build_select_clause(columns: Dict[str, List[str]], extra: Optional[List[str]] = None) -> str:
    """
    Build a SELECT clause with qualified names and safe fallbacks for missing columns.
    """
    select_cols = []
    # Example: coloc.h4, credible.studyId, study.traitFromSource
    for table, cols in columns.items():
        for col in cols:
            select_cols.append(f"{table}.{col} AS {table}__{col}")
    if extra:
        for col in extra:
            found = False
            for table, cols in columns.items():
                if col in cols:
                    select_cols.append(f"{table}.{col} AS {col}")
                    found = True
            if not found:
                select_cols.append(f"CAST(NULL AS VARCHAR) AS {col}")
    return ",\n  ".join(select_cols)

def build_query(paths: Dict[str, str], h4_threshold: float, select_clause: str, full: bool = True) -> str:
    """
    Build the DuckDB SQL query for colocalization extraction.
    """
    query = f"""
SELECT
  {select_clause}
FROM (
  SELECT * FROM read_parquet('{paths['coloc']}')
  WHERE h4 >= {h4_threshold}
) coloc
LEFT JOIN read_parquet('{paths['credible']}') credible
  ON coloc.rightStudyLocusId = credible.studyLocusId
LEFT JOIN read_parquet('{paths['study']}') study
  ON credible.studyId = study.studyId
WHERE credible.studyId IS NOT NULL
ORDER BY coloc.h4 DESC
"""
    if not full:
        query += "\nLIMIT 100"
    return query

def run_query_to_parquet(con: duckdb.DuckDBPyConnection, sql: str, out_dir: str, partition_cols: Optional[List[str]]):
    """
    Execute the query and write results to Parquet, partitioned if possible.
    """
    os.makedirs(out_dir, exist_ok=True)
    part_clause = ""
    if partition_cols:
        part_clause = f", PARTITION_BY {','.join(partition_cols)}"
    out_path = os.path.join(out_dir, "coloc_extract.parquet")
    copy_sql = f"""
COPY (
  {sql}
) TO '{out_path}' (FORMAT PARQUET{part_clause}, COMPRESSION ZSTD);
"""
    logging.info("Exporting results to Parquet...")
    con.execute(copy_sql)
    logging.info(f"Export complete: {out_path}")

def compute_summary_stats(con: duckdb.DuckDBPyConnection, out_dir: str, stats_out: str):
    """
    Compute summary statistics from the exported dataset.
    """
    parquet_path = os.path.join(out_dir, "coloc_extract.parquet")
    if not os.path.exists(parquet_path):
        raise FileNotFoundError(f"Exported Parquet not found: {parquet_path}")
    # Example summary: counts by studyId, traitFromSource, h4 distribution
    stats_sql = """
SELECT
  COUNT(*) AS total_rows,
  COUNT(DISTINCT study__studyId) AS n_studies,
  MIN(coloc__h4) AS h4_min,
  MEDIAN(coloc__h4) AS h4_median,
  APPROXIMATE_PERCENTILE(coloc__h4, 0.95) AS h4_p95,
  MAX(coloc__h4) AS h4_max
FROM read_parquet('{parquet_path}')
"""
    stats = con.execute(stats_sql.replace("{parquet_path}", parquet_path)).fetchdf()
    stats.to_parquet(stats_out)
    logging.info(f"Summary stats saved: {stats_out}")

def main():
    parser = argparse.ArgumentParser(description="GWAS–QTL Colocalization Extractor")
    parser.add_argument("--data-root", required=True)
    parser.add_argument("--h4-threshold", type=float, default=0.8)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--stats-out", required=True)
    parser.add_argument("--partition-cols", type=str, default="studyId,traitFromSource")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--select-extra", type=str, default="")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    duckdb_threads = args.threads
    con = duckdb.connect()
    con.execute(f"PRAGMA threads={duckdb_threads};")

    table_paths = {
        "coloc": os.path.join(args.data_root, "colocalisation_coloc.parquet"),
        "credible": os.path.join(args.data_root, "credible_set.parquet"),
        "study": os.path.join(args.data_root, "study.parquet"),
    }

    columns = discover_columns(con, table_paths)
    extra_cols = args.select_extra.split(",") if args.select_extra else []
    select_clause = build_select_clause(columns, extra=extra_cols)
    query = build_query(table_paths, args.h4_threshold, select_clause, full=True)

    # Save query for provenance
    with open(os.path.join(args.out_dir, "query.sql"), "w") as f:
        f.write(query)

    # Save schema
    import json
    with open(os.path.join(args.out_dir, "schema.json"), "w") as f:
        json.dump(columns, f, indent=2)

    partition_cols = [c for c in args.partition_cols.split(",") if c]
    run_query_to_parquet(con, query, args.out_dir, partition_cols)
    compute_summary_stats(con, args.out_dir, args.stats_out)

if __name__ == "__main__":
    main()
