# OpenTargets Coloc Analysis

This project provides tools for computing GWAS-QTL colocalization extracts and summary statistics. It is designed to be memory-safe and parameterized, allowing for efficient analysis of genetic data.

## Overview

The OpenTargets Coloc Analysis module allows users to extract and summarize colocalization data from GWAS and QTL datasets. The main functionalities include:

- Extracting colocalization data from Parquet files.
- Computing summary statistics from the extracted data.
- Providing a command-line interface for ease of use.

## Installation

To install the required dependencies, you can use pip. First, clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd opentargets_coloc_analysis
```

Then, install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

You can run the analysis using the command line. The basic usage is as follows:

```bash
python -m src.cli --help
```

This will display the available options and parameters for the analysis.

### Example Command

To perform a colocalization analysis, you can use a command like:

```bash
python -m src.cli --input <input_parquet_file> --output <output_directory> --h4_threshold <threshold_value>
```

Replace `<input_parquet_file>`, `<output_directory>`, and `<threshold_value>` with your specific parameters.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.