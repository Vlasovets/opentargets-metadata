def main():
    import argparse
    from coloc.extract import run_query_to_parquet, compute_summary_stats

    parser = argparse.ArgumentParser(description="GWAS-QTL Colocalization Analysis")
    parser.add_argument('--db', required=True, help='Path to the database file')
    parser.add_argument('--output-dir', required=True, help='Directory to save output files')
    parser.add_argument('--h4-threshold', type=float, default=0.01, help='H4 threshold for colocalization')
    parser.add_argument('--full', action='store_true', help='Flag to indicate full extraction without limits')

    args = parser.parse_args()

    # Establish database connection
    import duckdb
    con = duckdb.connect(args.db)

    # Discover columns and build query
    table_paths = {'your_table_name': args.db}  # Replace with actual table names
    columns = discover_columns(con, table_paths)
    select_clause = build_select_clause(columns)
    sql_query = build_query(table_paths, args.h4_threshold, select_clause, args.full)

    # Run query and compute summary statistics
    run_query_to_parquet(con, sql_query, args.output_dir, partition_cols=None)
    compute_summary_stats(con, args.output_dir, 'summary_stats.csv')

    con.close()

if __name__ == "__main__":
    main()