# Evidence-to-Claim Traceability Table

| # | Manuscript claim | Evidence | Evidence type | Reproducible? | Limitation |
|---|---|---|---|---|---|
| 1 | Delta Lake supports schema enforcement and controlled schema evolution (mergeSchema/autoMerge) | docs.delta.io; Databricks schema-enforcement docs | External fact (primary/official docs) | N/A (documentation) | Product docs may change; re-verify before submission if delayed |
| 2 | ODCS v3.2.0 is the current version of the standard | docs.datacontract.com/open-data-contract-standard; bitol-io.github.io | External fact (primary/official docs) | N/A | Standards version; re-verify at submission time |
| 3 | NYC TLC added `cbd_congestion_fee` to Yellow/Green/HVFHV for 2025 onward | nyc.gov/site/tlc official trip-record page | External fact (primary/government source) | N/A | Stable historical fact, low risk of change |
| 4 | Montana et al. describe data contracts as types in a production composable lakehouse | arXiv:2607.13339 (pre-print accepted at CDMS @ VLDB 2026) | External fact (peer-reviewed workshop pre-print) | N/A | Pre-print; confirm final venue/proceedings citation once published |
| 5 | Schema-only detector: TP=90, FP=0, FN=210, TN=100; precision 1.000, recall 0.300, F1 0.462, accuracy 0.475 | `results/raw_metrics.json`, `src/run_experiment.py` | Measured result (controlled/synthetic) | Yes — seed 42 | Closed-world coverage, not predictive accuracy |
| 6 | Contract-aware detector: TP=210, FP=0, FN=90, TN=100; precision 1.000, recall 0.700, F1 0.824, accuracy 0.775 | `results/raw_metrics.json` | Measured result (controlled/synthetic) | Yes — seed 42 | Same as above |
| 7 | Metadata-aware detector: TP=300, FP=0, FN=0, TN=100; all metrics 1.000 | `results/raw_metrics.json` | Measured result (controlled/synthetic) | Yes — seed 42 | Perfect result is closed-world rule coverage by construction, explicitly flagged as such in Sections 6 and 8 |
| 8 | 95% bootstrap CIs for recall/F1 per detector | `results/raw_metrics.json` (3,000 resamples, seed 42) | Measured result (controlled/synthetic) | Yes | Not applicable in v2.1 -- CIs are now bit-identical to the shipped script (see REPRODUCTION_NOTE.md) |
| 9 | Component-level timing (p50/p95/mean, ms per 400 cases) | `results/raw_metrics.json`, local timing harness | Environment-sensitive measured result | Partially (absolute values vary by machine) | Explicitly labeled as non-production, local Python dispatch only |
| 10 | Independent reproduction reproduced identical confusion-matrix counts | `docs/REPRODUCTION_NOTE.md` | Archival artifact / measured result | Yes | Documents both agreement and expected minor bootstrap/timing differences |
| 11 | Detection rate by violation type (Figure 3 matrix) | `results/raw_metrics.json` → `detection_by_violation_type` | Measured result (controlled/synthetic) | Yes | Same closed-world caveat as items 5-7 |

No major numerical conclusion in the manuscript lacks a traceable source in this table.
