# Product Context: CS-KG 2.0

## Problem Statement

Researchers and developers need a structured, queryable knowledge graph of computer science research that captures entities, relationships, and temporal context from academic literature. Manual extraction is infeasible at scale.

## Solution Approach

Automated pipeline that:
1. Ingests OpenAlex research paper data
2. Extracts entities and relationships using ML models
3. Validates triples using fine-tuned transformers
4. Maps to standard ontologies
5. Enriches with context and temporal information
6. Exports as queryable knowledge graph

## User Experience Goals

### Primary Users
- Researchers analyzing CS research trends
- Developers building on top of CS-KG
- Data scientists exploring academic networks

### User Workflows

**Workflow 1: Process New Research Data**
1. Add OpenAlex JSONL files to data/original
2. Run preprocessing script
3. Execute extraction pipeline (DyGIE++, CoreNLP)
4. Run construction and validation steps
5. Apply ontology mapping
6. Add context/time information
7. Export final knowledge graph

**Workflow 2: Customize Validation Thresholds**
1. Download pre-trained model OR fine-tune on custom data
2. Adjust SUPPORT_S1 and SUPPORT_S2 thresholds
3. Apply model to generated triples
4. Evaluate quality of filtered results

**Workflow 3: Query Existing Knowledge Graph**
1. Access SPARQL endpoint at https://scholkg.kmi.open.ac.uk/
2. Query for entities, relationships, or patterns
3. Download dump files if needed

## Key User Stories

1. **As a researcher**, I want to process my own OpenAlex data so that I can create a custom knowledge graph for my domain
2. **As a data scientist**, I want to adjust validation thresholds so that I can control the precision/recall trade-off
3. **As a developer**, I want CSV and RDF outputs so that I can integrate the knowledge graph into my application
4. **As a pipeline user**, I want clear error messages so that I can debug issues in the multi-stage process

## Success Metrics

- Pipeline completion rate for sample data: 100%
- Triple validation accuracy: Per paper metrics
- Processing time: Acceptable for research use
- Data quality: Manual spot-checks validate correctness
- Reproducibility: Other researchers can replicate results
