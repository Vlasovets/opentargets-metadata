# OpenTargets Data Analysis

## Overview

This repository contains metadata and analysis results for studies using [OpenTargets Platform](https://platform.opentargets.org/) data. It is a part of ongoing research into the genetic basis of human disease and drug target identification using population-scale genomic data.

### Analysis Scripts

#### Colocalization Analysis
- **Primary Function**: `analyze_gwas_colocalizations_with_available_columns()`
  - Creates comprehensive colocalization datasets with dynamic column selection
  - Filters for high-confidence colocalizations (H4 > 0.8)
  - Joins colocalization evidence with credible sets and study metadata
  - Provides detailed statistical analysis including:
    - Variant count analysis (`numberColocalisingVariants`)
    - Trans-QTL vs Cis-QTL breakdown (`isTransQtl`)
    - Colocalization hypothesis probabilities (H0-H4)
    - Study type distributions (GWAS, eQTL, pQTL)

#### Gene-Drug-Target Analysis
- **Primary Function**: `create_gene_drug_target_dataframe()`
  - Links genetic loci to genes and their drug targets
  - Combines locus-to-gene predictions with drug-target associations
  - Includes clinical development phase information where available
  - Provides comprehensive gene-drug mapping analysis

### Key Datasets Used

#### Core Colocalization Data
- **`colocalisation_coloc`**: Statistical evidence for shared causal variants between trait pairs
  - Columns: `leftStudyLocusId`, `rightStudyLocusId`, `chromosome`, `h0-h4`, `rightStudyType`, `numberColocalisingVariants`
- **`credible_set`**: Fine-mapped genetic variants with high causal probability
  - Columns: `studyLocusId`, `studyId`, `variantId`, `isTransQtl`
- **`study`**: Study metadata and trait descriptions
  - Columns: `studyId`, `studyType`, `traitFromSource`, `projectId`, `pubmedId`

#### Gene-Drug-Target Data
- **`l2g_prediction`**: Locus-to-gene mapping predictions
  - Columns: `studyLocusId`, `geneId`, `score`
- **`evidence`**: Target-disease association evidence
  - Columns: `studyId`, `targetId`, `diseaseId`
- **`known_drug`**: Known drug-target associations
  - Columns: `targetId`, `diseaseId`, `drugId`
- **`target`**: Gene/target annotations and symbols
  - Columns: `id`, `approvedSymbol`, `biotype`
- **`disease`**: Disease ontology and descriptions
  - Columns: `id`, `name`, `description`

### Data Processing Pipeline

1. **Schema Detection**: Dynamically checks available columns in each dataset
2. **Column Filtering**: Extracts only specified columns from large source datasets
3. **Memory Management**: Uses sampling and batch processing for large datasets
4. **Quality Control**: Filters for high-confidence associations and complete data
5. **Statistical Analysis**: Provides comprehensive summaries and cross-tabulations

### Output Files

#### Colocalization Results
- **`colocalisation_available_columns_with_variants.csv`**: Main colocalization analysis results
  - High-confidence genetic colocalizations (H4 > 0.8)
  - Includes variant-level information and QTL classifications
  - Cross-referenced with study metadata and trait descriptions

#### Gene-Drug-Target Results  
- **`gene_drug_target_associations.csv`**: Gene-to-drug target mappings
  - Links genetic associations to druggable targets
  - Includes gene symbols, drug identifiers, and development phases
  - Filtered for high-confidence locus-to-gene predictions (score > 0.5)

### Colocalization Methodology

The analysis implements Bayesian colocalization testing with five hypotheses:
- **H0**: No association at locus for either trait
- **H1**: Association for trait 1 only (typically GWAS)
- **H2**: Association for trait 2 only (typically QTL)
- **H3**: Both traits associated but different causal variants
- **H4**: Both traits associated with shared causal variant (**colocalization**)

High-confidence colocalizations are defined as H4 > 0.8, indicating >80% posterior probability of shared causal variants.

## Requirements

- Python 3.8+
- DuckDB
- pandas
- pyarrow
- pathlib

## Data Sources
- [OpenTargets Platform](https://platform.opentargets.org/)
- Data version: 29.07 (July 2025)

## References

- Mountjoy E, et al. (2021). An open approach to systematically prioritize causal variants and genes at all published human GWAS trait-associated loci. *Nature Genetics*, 53(11), 1527-1533.
- Giambartolomei C, et al. (2014). Bayesian test for colocalisation between pairs of genetic association studies using summary statistics. *PLoS Genetics*, 10(5), e1004383.