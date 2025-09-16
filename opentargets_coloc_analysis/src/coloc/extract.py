def discover_columns(con, table_paths: dict) -> dict[str, list[str]]:
    columns = {}
    for table_name, path in table_paths.items():
        query = f"SELECT * FROM '{path}' LIMIT 1"
        result = con.execute(query).fetchdf()
        columns[table_name] = result.columns.tolist()
    return columns

def build_select_clause(columns: dict) -> str:
    select_clauses = []
    for table_name, cols in columns.items():
        qualified_cols = [f"{table_name}.{col}" for col in cols]
        select_clauses.extend(qualified_cols)
    return ", ".join(select_clauses)

def build_query(paths: dict, h4_threshold: float, select_clause: str, full: bool = True) -> str:
    base_query = f"SELECT {select_clause} FROM "
    table_queries = [f"'{path}'" for path in paths.values()]
    full_query = base_query + " UNION ALL ".join(table_queries)
    if full:
        return full_query
    else:
        return f"{full_query} LIMIT 1000"

def run_query_to_parquet(con, sql: str, out_dir: str, partition_cols: list[str] | None):
    df = con.execute(sql).fetchdf()
    output_path = f"{out_dir}/output.parquet"
    df.to_parquet(output_path, partition_cols=partition_cols)

def compute_summary_stats(con, out_dir: str, stats_out: str):
    query = "SELECT COUNT(*) AS total_records FROM 'output.parquet'"
    total_records = con.execute(query).fetchone()[0]
    summary_stats = {
        "total_records": total_records,
        # Add more summary statistics as needed
    }
    summary_df = pd.DataFrame([summary_stats])
    summary_df.to_csv(f"{out_dir}/{stats_out}.csv", index=False)