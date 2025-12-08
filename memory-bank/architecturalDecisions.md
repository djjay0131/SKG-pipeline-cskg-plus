# Architectural Decisions

This file tracks significant architectural and technical decisions made throughout the project lifecycle.

## Decision Format

Each decision should include:
- **Date:** When the decision was made
- **Status:** Proposed | Accepted | Deprecated | Superseded
- **Context:** What prompted this decision
- **Decision:** What was decided
- **Consequences:** Impact and trade-offs
- **Alternatives Considered:** Other options evaluated

---

## ADR-001: Pipeline Architecture - Sequential Stages

**Date:** [Historical - predates current work]
**Status:** Accepted

**Context:**
Need to process research papers through multiple NLP and ML stages to produce knowledge graph.

**Decision:**
Implement sequential pipeline with clear stage boundaries:
1. Data Preparation → 2. Extraction → 3. Construction → 4. Validation → 5. Mapping → 6. Enrichment → 7. Export

**Consequences:**
- Pros: Clear separation of concerns, easy to debug individual stages, can optimize each stage independently
- Cons: Can't skip stages, longer total processing time, intermediate data storage needed
- Impact: Easy maintenance but sequential processing requirement

**Alternatives Considered:**
- End-to-end neural model: Rejected due to lack of interpretability and training data requirements
- Parallel processing: Not feasible due to stage dependencies

---

## ADR-002: Dual NLP Framework (DyGIE++ and CoreNLP)

**Date:** [Historical - predates current work]
**Status:** Accepted

**Context:**
Need comprehensive entity and relation extraction from scientific text.

**Decision:**
Use both DyGIE++ and CoreNLP for complementary coverage.

**Consequences:**
- Pros: Better entity coverage, robust linguistic processing
- Cons: Two frameworks to maintain, longer processing time
- Impact: Higher quality extraction at cost of complexity

**Alternatives Considered:**
- Single framework (either DyGIE++ or CoreNLP): Rejected due to coverage gaps
- Modern transformer-only approach: Considered but DyGIE++ specialized for scientific text

---

## ADR-003: Transformer-Based Validation

**Date:** [Historical - predates current work]
**Status:** Accepted

**Context:**
Need to filter low-quality or incorrect triples from automated extraction.

**Decision:**
Use fine-tuned SciBERT model with configurable thresholds (SUPPORT_S1, SUPPORT_S2).

**Consequences:**
- Pros: Effective filtering, domain-adapted (SciBERT), tunable precision/recall
- Cons: Requires model download/training, computationally expensive
- Impact: Higher quality knowledge graph, longer processing time

**Alternatives Considered:**
- Rule-based filtering: Too brittle, hard to maintain
- Manual validation: Not scalable
- Generic BERT: Less effective than domain-specific SciBERT

---

## ADR-004: Documentation Structure - Memory Bank + Construction

**Date:** 2025-12-01
**Status:** Accepted

**Context:**
Need robust documentation system that survives context resets and tracks active development.

**Decision:**
Implement two-folder system:
- `memory-bank/`: Persistent knowledge, context retention (6 core files)
- `construction/`: Active development tracking (design, requirements, sprints)

**Consequences:**
- Pros: Clear separation between persistent and active knowledge, systematic context recovery, structured development tracking
- Cons: Requires discipline to maintain, duplication risk if not careful
- Impact: Better context retention, clearer development workflow

**Alternatives Considered:**
- Single docs/ folder: Rejected, lacks separation between persistent and active contexts
- Wiki or external tool: Rejected, want everything in repository
- No formal structure: Rejected, context loss too severe

---

## ADR-005: Spec Builder Template with TodoWrite

**Date:** 2025-12-01
**Status:** Accepted

**Context:**
Need consistent approach to feature specification and requirements gathering.

**Decision:**
Use TodoWrite-driven workflow with 9-phase spec builder template including stakeholder question generation.

**Consequences:**
- Pros: Consistent specifications, systematic requirements gathering, stakeholder perspective built-in
- Cons: May be overhead for small features
- Impact: Higher quality specs, reduced ambiguity, better planning

**Alternatives Considered:**
- Ad-hoc specifications: Rejected, inconsistent quality
- Heavyweight formal methods: Rejected, too much overhead for research project
- User story templates only: Rejected, lacks technical depth

---

## Template for Future Decisions

```markdown
## ADR-XXX: [Decision Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded

**Context:**
[What is the issue that we're seeing that is motivating this decision or change?]

**Decision:**
[What is the change that we're actually proposing or doing?]

**Consequences:**
- Pros: [Positive outcomes]
- Cons: [Negative outcomes or trade-offs]
- Impact: [Overall impact on the project]

**Alternatives Considered:**
- [Alternative 1]: [Why rejected]
- [Alternative 2]: [Why rejected]
```

---

## Notes

- Update this file when making significant technical or architectural decisions
- Reference ADR numbers in code comments when implementing decisions
- Mark decisions as Deprecated or Superseded when they change, don't delete them
- Keep historical context even when decisions change
