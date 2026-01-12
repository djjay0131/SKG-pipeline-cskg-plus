# Dockerfile for CS-KG Pipeline (Construction, Validation, Post-processing)
# For extraction, use the DyGIE++ container in src/extraction/dygiepp/

FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PYTHONPATH=/workspace/src:/workspace/src/construction:$PYTHONPATH

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    unzip \
    build-essential \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

# Create working directory
WORKDIR /workspace

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4')"

# Create necessary directories
RUN mkdir -p /workspace/data/original \
    /workspace/data/processed \
    /workspace/data/processed/dygiepp_input \
    /workspace/data/processed/dygiepp_output \
    /workspace/data/processed/cso_output \
    /workspace/data/processed/extracted_triples \
    /workspace/data/processed/other_info \
    /workspace/csv_release \
    /workspace/rdf_release

# Copy the project files (excluding large files via .dockerignore)
COPY src/ /workspace/src/

# Set working directory to workspace
WORKDIR /workspace

# Default command - run bash shell
CMD ["/bin/bash"]
