import argparse
from opentargets_coloc_analysis.src.main import main

def create_cli():
    parser = argparse.ArgumentParser(description="GWAS-QTL Colocalization Analysis")
    parser.add_argument(
        '--input', 
        type=str, 
        required=True, 
        help='Path to the input data file or directory containing Parquet files.'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        required=True, 
        help='Directory where the output files will be saved.'
    )
    parser.add_argument(
        '--h4-threshold', 
        type=float, 
        default=0.01, 
        help='H4 threshold for colocalization analysis (default: 0.01).'
    )
    parser.add_argument(
        '--full', 
        action='store_true', 
        help='If set, run the full analysis without sampling.'
    )

    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    create_cli()