# Docker Setup for CS-KG Pipeline

This document explains how to build and run the CS-KG pipeline using Docker.

## Prerequisites

- Docker Desktop installed and running
- At least 8GB of RAM available for Docker
- Sufficient disk space (~10GB for images and data)

## Quick Start

### 1. Build the Docker Image

```powershell
docker-compose build
```

Or build directly:

```powershell
docker build -t cskg-pipeline .
```

### 2. Start the Container

```powershell
docker-compose up -d
```

### 3. Access the Container

```powershell
docker-compose exec cskg-pipeline /bin/bash
```

Or if using docker directly:

```powershell
docker run -it --rm -v ${PWD}:/workspace cskg-pipeline /bin/bash
```

## Running the Pipeline

Once inside the container, follow the standard pipeline workflow:

### Step 1: Data Preparation

```bash
cd /workspace/src/extraction
python preprocess.py
```

### Step 2: Entity Extraction

```bash
# Prepare data for DyGIE++
python data_preparation_dygiepp.py

# Run DyGIE++ extraction
bash run_dygiepp.sh

# Run CoreNLP extraction
bash run_corenlp.sh
```

### Step 3: Triple Construction

```bash
cd /workspace/src/construction
python cskg_construction.py
```

### Step 4: Validation (Option A - Pre-trained Model)

First, download the pre-trained model from [Zenodo](https://zenodo.org/record/6628472) and place it in `src/transformer/tuned-transformer/`

```bash
cd /workspace/src/transformer
python applyModel.py tuned-transformer/ 3 3
```

### Step 4: Validation (Option B - Fine-tune Your Own)

```bash
cd /workspace/src/transformer
python prepareTrainingData.py 3 3
python finetuner.py
python applyModel.py tuned-transformer/ 3 3
```

### Step 5: Ontology Mapping

```bash
cd /workspace/schema_validation
python apply_onto.py
```

### Step 6: Post-processing

```bash
cd /workspace/postprocessing
python 1_triple_selector.py
python 2_context.py
python 3_compute_support_entity.py
python 4_create_rdf.py
```

## Volume Mounts

The docker-compose.yml file mounts the following directories:

- `./data` → `/workspace/data` - Input and intermediate data
- `./src` → `/workspace/src` - Source code
- `./resources` → `/workspace/resources` - Resource files
- `./csv_release` → `/workspace/csv_release` - CSV outputs
- `./rdf_release` → `/workspace/rdf_release` - RDF outputs

This allows you to:
- Access generated files from your host machine
- Edit code on your host and run it in the container
- Persist data between container restarts

## Troubleshooting

### Container Won't Start

Check Docker Desktop is running and has sufficient resources allocated.

### Out of Memory Errors

Increase memory allocation in docker-compose.yml or Docker Desktop settings.

### Permission Issues

On Windows, ensure Docker has access to the drive where the project is located.

### Missing Dependencies

If you encounter import errors, rebuild the image:

```powershell
docker-compose build --no-cache
```

### CoreNLP Not Found

The Dockerfile should download CoreNLP automatically. If it fails:

```bash
cd /workspace/src/extraction
wget http://nlp.stanford.edu/software/stanford-corenlp-4.5.4.zip
unzip stanford-corenlp-4.5.4.zip
rm stanford-corenlp-4.5.4.zip
```

## Development Workflow

### Interactive Development

1. Start container: `docker-compose up -d`
2. Access shell: `docker-compose exec cskg-pipeline /bin/bash`
3. Edit files on your host machine
4. Run code inside the container
5. View outputs on your host machine

### Running Individual Scripts

```powershell
docker-compose exec cskg-pipeline python /workspace/src/extraction/preprocess.py
```

### Stopping the Container

```powershell
docker-compose down
```

### Removing Everything (Clean Slate)

```powershell
docker-compose down -v
docker rmi cskg-pipeline
```

## Notes

- The container runs with Python 3.9 as specified in project requirements
- Java 11 is installed for Stanford CoreNLP
- NLTK data (punkt, stopwords, wordnet) is pre-downloaded
- The container uses `/workspace` as the working directory
- Environment variables can be configured in docker-compose.yml

## Resource Requirements

Recommended system resources:
- **CPU**: 4 cores
- **RAM**: 8GB minimum (16GB recommended)
- **Disk**: 10GB free space
- **GPU**: Optional (for faster transformer processing)

For GPU support, you would need to modify the Dockerfile to use a CUDA-enabled base image and install appropriate PyTorch versions.
