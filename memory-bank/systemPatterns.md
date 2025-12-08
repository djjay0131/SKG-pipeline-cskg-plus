# System Patterns: CS-KG Pipeline Architecture

## System Architecture

### High-Level Components

```
[OpenAlex Data]
    ↓
[Data Preparation] (src/extraction/preprocess.py)
    ↓
[Entity Extraction] (DyGIE++ + CoreNLP)
    ↓
[Triple Construction] (src/construction/cskg_construction.py)
    ↓
[Triple Validation] (SciBERT Transformer)
    ↓
[Ontology Mapping] (schema_validation/)
    ↓
[Context Enrichment] (postprocessing/)
    ↓
[Export] (CSV + RDF/Turtle)
```

## Implementation Phases

### Phase 1: Data Preparation
**Location:** `/src/extraction/`
- Input: OpenAlex JSONL files in `data/original/`
- Process: Run `preprocess.py`
- Output: Cleaned, structured data ready for extraction

### Phase 2: Entity Extraction - DyGIE++
**Location:** `/src/extraction/`
- Process: Run `data_preparation_dygiepp.py` then `run_dygiepp.sh`
- Purpose: Extract named entities and relationships from text
- Output: Entity annotations

### Phase 3: Entity Extraction - CoreNLP
**Location:** `/src/extraction/`
- Process: Run `run_corenlp.sh`
- Purpose: Additional linguistic processing and entity recognition
- Output: Linguistic annotations

### Phase 4: Triple Construction
**Location:** `/src/construction/`
- Process: Run `cskg_construction.py`
- Tasks:
  - Clean and merge entities
  - Map entities to external resources
  - Map verbs/predicates
  - Generate candidate triples
- Output: Raw triples for validation

### Phase 5: Triple Validation
**Location:** `/src/transformer/`
- **Option A (Use Pre-trained):**
  - Download model from Zenodo
  - Run `applyModel.py tuned-transformer/ 3 3`
- **Option B (Fine-tune):**
  - Run `prepareTrainingData.py SUPPORT_S1 SUPPORT_S2`
  - Run `finetuner.py`
  - Run `applyModel.py MODEL_NAME SUPPORT_S1 SUPPORT_S2`
- Purpose: Filter triples based on confidence thresholds
- Output: Validated triples

### Phase 6: Ontology Mapping
**Location:** `/schema_validation/`
- Process: Run `apply_onto.py`
- Purpose: Map entities and relationships to standard ontology
- Output: Ontology-aligned triples

### Phase 7: Context and Temporal Enrichment
**Location:** `/postprocessing/`
- Process (sequential):
  1. `1_triple_selector.py`
  2. `2_context.py`
  3. `3_compute_support_entity.py`
  4. `create_rdf.py`
- Purpose: Add publication context, time information, compute entity support
- Output: Final knowledge graph in `csv_release/` and `rdf_release/`

## Design Patterns

### Pipeline Pattern
Sequential processing stages with clear input/output contracts between stages.

### Batch Processing
Process multiple JSONL files in parallel where possible.

### Configurable Thresholds
SUPPORT_S1 and SUPPORT_S2 parameters allow quality tuning.

### Model Flexibility
Support both pre-trained and custom fine-tuned models.

## Critical Code Paths

### Main Pipeline Flow
1. `src/extraction/preprocess.py` - Entry point for data prep
2. `src/extraction/data_preparation_dygiepp.py` - DyGIE++ setup
3. `src/construction/cskg_construction.py` - Triple generation
4. `src/transformer/applyModel.py` - Validation
5. `schema_validation/apply_onto.py` - Ontology alignment
6. `postprocessing/create_rdf.py` - Final export

### Directory Structure
```
data/
  original/          # Input OpenAlex JSONL files
  [intermediate/]    # Generated during processing
src/
  extraction/        # Data prep and entity extraction
  construction/      # Triple generation
  transformer/       # Validation with SciBERT
schema_validation/   # Ontology mapping
postprocessing/      # Final enrichment
csv_release/         # CSV output
rdf_release/         # RDF/Turtle output
```

## Technical Decisions

### Why DyGIE++ and CoreNLP?
- DyGIE++ excels at domain-specific entity and relation extraction
- CoreNLP provides robust linguistic processing
- Combination provides comprehensive coverage

### Why SciBERT for Validation?
- Pre-trained on scientific literature
- Effective at identifying valid scientific relationships
- Fine-tunable for domain-specific needs

### Why Configurable Thresholds?
- Different use cases need different precision/recall trade-offs
- Research validation vs. production deployment needs
- Allows empirical optimization

## Component Relationships

```
Preprocessing → Extraction → Construction → Validation → Mapping → Enrichment → Export
     ↓              ↓             ↓              ↓           ↓          ↓
  [Clean]      [Entities]    [Triples]     [Filtered]  [Aligned]  [Final KG]
```

Each stage depends on the previous stage's output. No stage can be skipped.
