# Active Context

**Last Updated:** 2025-12-01

## Current Work Phase

Setting up project documentation structure with memory-bank and construction folders.

## Immediate Next Steps

1. Complete initialization of memory-bank core files
2. Design agent automation for documentation management
3. Consider initial population of architectural decisions

## Recent Decisions

### Decision 1: Documentation Structure
- **Date:** 2025-12-01
- **Decision:** Implement dual-folder system: memory-bank for knowledge retention, construction for active development
- **Rationale:** Separation of concerns - memory-bank maintains context across sessions, construction tracks current development state
- **Impact:** Clear organization for documentation, easier context recovery after interruptions

### Decision 2: Spec Builder Template
- **Date:** 2025-12-01
- **Decision:** Use TodoWrite-driven workflow for feature specifications
- **Rationale:** Ensures systematic approach to gathering requirements and designing features
- **Impact:** Consistent specification quality, reduced ambiguity in requirements

## Key Patterns and Preferences

### Documentation Patterns
- Use markdown for all documentation
- Include checklists for actionable items
- Cross-reference between related documents
- Update activeContext.md after every significant change

### Development Patterns
- Follow existing Python 3.9 codebase conventions
- Maintain pipeline modularity (each stage independent)
- Use command-line arguments for configuration
- Shell scripts for orchestrating complex processes

## Important Learnings

### About the Project
- CS-KG 2.0 is a research project for knowledge graph construction
- Pipeline has 7 distinct phases, each dependent on previous
- Quality controlled through transformer-based validation
- Sample data only - full dataset from OpenAlex

### About the Codebase
- Existing structure: src/extraction, src/construction, src/transformer
- Additional directories: schema_validation, postprocessing
- Uses pre-trained SciBERT model for validation
- Outputs to csv_release/ and rdf_release/

## Open Questions

1. Should we create automation agents for documentation updates?
2. How frequently should memory-bank be updated during development?
3. Are there existing architectural decision records to migrate?
4. Should we track issues/bugs in construction folder or separate system?

## Notes for Next Session

- Remember to read ALL memory-bank files on context reset
- Check progress.md to see what's completed
- Review construction/sprints/ for current development state
- Update this file before ending session
