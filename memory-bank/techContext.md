# Technical Context: CS-KG Pipeline

## Technologies and Frameworks

### Core Language
- **Python 3.9** - Required version for all scripts

### Machine Learning Models
- **DyGIE++** - Entity and relation extraction from scientific text
- **CoreNLP** - Linguistic processing and NLP tasks
- **SciBERT** - BERT model fine-tuned on scientific literature
  - Pre-trained model available: https://zenodo.org/record/6628472

### Data Format
- **Input:** OpenAlex JSONL (JSON Lines) format
- **Output:** CSV and RDF/Turtle formats

### External Resources
- **OpenAlex** - Source of research paper metadata (https://openalex.org/)
- **Ontologies** - Standard ontologies for CS domain mapping

## Development Environment Setup

### Prerequisites
1. Python 3.9 installed
2. Required Python libraries (see requirements if available)
3. DyGIE++ model files
4. CoreNLP installation
5. Pre-trained transformer model (download from Zenodo)

### Directory Setup
```bash
# Clone repository
git clone <repo-url>
cd SKG-pipeline-cskg-plus

# Create data directory
mkdir -p data/original

# Download transformer model
# Extract to src/transformer/tuned-transformer/
```

### Running the Pipeline

**Step 1: Data Preparation**
```bash
cd src/extraction
python preprocess.py
```

**Step 2: Extraction**
```bash
python data_preparation_dygiepp.py
./run_dygiepp.sh
./run_corenlp.sh
```

**Step 3: Construction**
```bash
cd ../construction
python cskg_construction.py
```

**Step 4: Validation (Option A - Pre-trained)**
```bash
cd ../transformer
python applyModel.py tuned-transformer/ 3 3
```

**Step 4: Validation (Option B - Fine-tune)**
```bash
cd ../transformer
python prepareTrainingData.py 3 3
python finetuner.py
python applyModel.py tuned-transformer/ 3 3
```

**Step 5: Ontology Mapping**
```bash
cd ../../schema_validation
python apply_onto.py
```

**Step 6: Post-processing**
```bash
cd ../postprocessing
python 1_triple_selector.py
python 2_context.py
python 3_compute_support_entity.py
python create_rdf.py
```

## Code Patterns and Conventions

### File Organization
- Extraction code: `src/extraction/`
- Construction logic: `src/construction/`
- Validation: `src/transformer/`
- Schema validation: `schema_validation/`
- Post-processing: `postprocessing/`

### Naming Conventions
- Scripts use snake_case: `cskg_construction.py`
- Shell scripts: `run_dygiepp.sh`
- Data directories: lowercase with underscores

### Configuration
- Thresholds: SUPPORT_S1 and SUPPORT_S2 command-line parameters
- Model path: First parameter to applyModel.py
- Input data: `data/original/` directory

## Common Issues and Debugging

### Issue: Missing Dependencies
**Symptom:** Import errors or module not found
**Solution:** Check Python 3.9 is active, install required libraries

### Issue: Model Not Found
**Symptom:** FileNotFoundError for transformer model
**Solution:** Download model from Zenodo and extract to `src/transformer/tuned-transformer/`

### Issue: Empty Output
**Symptom:** No files in csv_release/ or rdf_release/
**Solution:** Check each pipeline stage completed successfully, review logs

### Issue: Script Execution Order
**Symptom:** Errors due to missing intermediate files
**Solution:** Follow exact order in README.md, don't skip stages

### Issue: Data Format
**Symptom:** Parsing errors in preprocessing
**Solution:** Verify OpenAlex data is in JSONL format, check sample data

## Testing Strategy

### Unit Testing
Currently not implemented - opportunity for improvement

### Integration Testing
Run pipeline on sample data provided in repository

### Validation
Manual spot-checks of:
- Entity extraction accuracy
- Triple quality
- Ontology mapping correctness
- Final RDF/CSV format validity

## Performance Considerations

- Processing time depends on dataset size
- Each stage processes all papers sequentially
- Transformer validation is most time-intensive
- Consider parallel processing for large datasets

## Dependencies

### Python Libraries
(Check repository for requirements.txt or setup.py)
- Likely includes: transformers, torch, numpy, pandas, etc.

### External Tools
- DyGIE++ model files
- CoreNLP Java libraries
- Shell environment (bash) for .sh scripts

## Platform Notes

- Developed and tested on Linux/Unix systems
- Shell scripts (.sh) may need adaptation for Windows
- Path separators and command syntax may differ by platform
