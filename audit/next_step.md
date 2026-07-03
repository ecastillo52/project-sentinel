# Phase 2 — Architectural Consolidation.

Order of Operation:
-



---
Phase 2.1 — Execution blockers ✅
-
    ✅ find_by_hash() restored
    ✅ duplicate health.py removed
    ✅ duplicate metadata/hashing.py removed
    ✅ single hashing implementation (core/utils/hash.py)
    ✅ single Health implementation (HealthEngine)
    ✅ application launches again



---
Phase 2.2 — Remove duplicate implementations ✅
-

    🟩 old metadata/hashing.py 
    🟩 old health.py


---

Phase 2.3 - Complete Domain Model Transition ✅
-

~~This is where we stop talking about files and start talking about models.~~

~~Specifically, we remove the last pieces of "legacy dictionary programming."~~

EDIT: 

This phase removes the last remnants of legacy dictionary-based programming and completes Sentinel's transition to an object-oriented domain model.


From the audit, these are the remaining architectural improvements:

- ~~core/intelligence/recommendations.py still operates on nested dictionaries instead of Report/Sensor objects.~~
- ~~core/engine/summary.py has a couple of helpers that still depend on serialized structures rather than the domain models.~~
- ~~core/intelligence/metrics.py duplicates sensor IDs in multiple places, which could be centralized through the sensor registry.~~
- ~~core/intelligence/insights.py has some helper logic that overlaps with metrics.py.~~

EDIT:

- core/intelligence/recommendations.py should consume Report and Sensor models instead of nested dictionaries.
- core/engine/summary.py should operate on Report data instead of serialized structures where possible.
- core/intelligence/metrics.py should use the centralized sensor registry instead of duplicating sensor identifiers.
- core/intelligence/insights.py should share common metric logic rather than duplicating helper functions.

~~Those changes will complete the transition to a consistently object-oriented domain model across Sentinel.~~

EDIT:

Result:

- Every major subsystem consumes the same domain models.
- Sensor definitions exist in one location.
- Business logic exists in one location.
- Serialization is confined to persistence and reporting.

NOTES:
- 1 genuine architecture migration (recommendations.py)
- 1 small API modernization (summary.py)
- 2 cleanup passes (metrics.py and insights.py)
- A handful of stale sensor ID bugs that likely came from the registry rename (cpu_temperature → cpu_temp, etc.).

---

    🟩 one hashing implementation
    🟩 one sensor registry
    🟩 one health engine
    🟩 remove obsolete legacy files

---
Phase 2.4  — Modernize Intelligence
-
The intelligence package should become a cohesive analysis layer instead of a collection of independent helper modules.

GOALS:

    ☐ eliminate duplicated historical-analysis logic
    ☐ centralize sensor access helpers
    ☐ centralize trend calculations
    ☐ reduce repeated iteration over Session history
    ☐ improve cohesion between metrics.py, insights.py, and report.py
    ☐ ensure intelligence depends only on Session/Report/Sensor models

---
Phase 2.5 Verify Layer Boundaries
-

Audit every package for responsibility.

Example:

    engine

🚧 Should never know about

    ui
    metadata

🚧 Should never know about

    report
    models

🚧 Should never import

    services
    database

---
Phase 2.6 — Final Polish
-

    🟥 typing
    🟥 naming consistency
    🟥 imports
    🟥 formatting
    🟥 docstrings
    🟥 technical debt
    🟥 comments
    🟥 helper ordering