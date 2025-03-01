#!/bin/bash
set -e

# Define variables for the data URL, output file, and extraction directory
DATA_URL="https://clinicaltrials.gov/AllPublicXML.zip"
OUTPUT_ZIP="clinicaltrials.zip"
DATA_DIR="data"

echo "Downloading ClinicalTrials.gov dataset from ${DATA_URL}..."
wget -O ${OUTPUT_ZIP} ${DATA_URL}

echo "Creating extraction directory (${DATA_DIR})..."
mkdir -p ${DATA_DIR}

echo "Extracting data..."
unzip -o ${OUTPUT_ZIP} -d ${DATA_DIR}

echo "Dataset downloaded and extracted to '${DATA_DIR}'."
# Script to download clinical trial data
