# Project Brief: SKG-pipeline-cskg-plus

## Core Objectives

Build and maintain a pipeline for constructing Computer Science Knowledge Graph (CS-KG 2.0) from OpenAlex research paper data.

## Requirements

### Functional Requirements
- Process OpenAlex JSONL data files
- Extract entities and relationships from research papers
- Generate validated knowledge graph triples
- Map entities to external resources and ontologies
- Produce CSV and RDF/Turtle outputs

### Technical Requirements
- Python 3.9 compatibility
- Integration with DyGIE++, CoreNLP, and SciBERT transformer models
- Support for batch processing of research papers
- Validation using fine-tuned transformer models

## Success Criteria

- [ ] Successfully processes OpenAlex data through all pipeline stages
- [ ] Generates validated triples with configurable support thresholds
- [ ] Produces exportable knowledge graph in CSV and RDF formats
- [ ] Maintains data quality through transformer-based validation
- [ ] Documentation enables reproducibility

## Project Constraints

### In Scope
- Pipeline for OpenAlex data processing
- Entity extraction and relationship mapping
- Triple validation and ontology mapping
- Context and temporal information integration
- Export to standard formats (CSV, RDF)

### Out of Scope
- Real-time processing
- Support for data sources other than OpenAlex
- Custom ontology development
- User interface or web application
- Full dataset distribution (sample only)

## Testing Checklist

- [ ] Data preprocessing completes without errors
- [ ] DyGIE++ extraction produces valid output
- [ ] CoreNLP processing succeeds
- [ ] Triple generation creates valid relationships
- [ ] Transformer validation applies correctly
- [ ] Ontology mapping completes
- [ ] Context and time information added
- [ ] Final CSV and RDF files generated
- [ ] Sample data test end-to-end successful

## Contact & Resources

- Primary Contact: Danilo Dessi (danilo.dessi@unica.it)
- Website: https://scholkg.kmi.open.ac.uk/
- Related Repository: https://github.com/danilo-dessi/SKG-pipeline
- Model Source: https://zenodo.org/record/6628472
- Data Source: https://openalex.org/
