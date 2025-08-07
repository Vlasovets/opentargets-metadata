# OpenTargets Data Analysis

## Overview

This repository contains metadata and analysis results for studies using [OpenTargets Platform](https://platform.opentargets.org/) data. It is a part of ongoing research into the genetic basis of human disease and drug target identification using population-scale genomic data.

## Repository Contents

### Metadata Files

#### `/metadata/json/`
- **`structured_catalog.json`**: Comprehensive catalog of all OpenTargets datasets with detailed schema information, column descriptions, and data types
- **`columns_manifest.json`**: Manifest of column definitions across datasets of choice
- **`catalog.txt`**: Simple text listing of available datasets
- **`by_dataset/`**: Individual JSON files containing dataset-specific metadata with example values

#### `/metadata/csv/`
- **`merged_output.csv`**: Colocalization analysis results containing:
  - `leftStudyLocusId`: Identifier for the first genetic locus
  - `rightStudyLocusId`: Identifier for the second genetic locus  
  - `studyId`: GWAS study identifier
  - `h4`: Posterior probability of shared causal variant (H4 hypothesis)
