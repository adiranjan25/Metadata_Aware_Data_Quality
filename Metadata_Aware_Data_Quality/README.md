# Reproducibility Package — Metadata-Aware Data Quality (Paper 2)

## Purpose
This package reproduces the controlled 400-case benchmark reported in:
"Metadata-Aware Data Quality: A Lightweight Framework for Detecting Schema
Drift and Data Contract Violations in Modern Data Pipelines" (FNU Aditya Ranjan).

## Exact experiment
- 400 cases: 100 clean controls + 300 injected violations across 10 classes (30 each)
- 3 deterministic rule-based detectors: schema-only, contract-aware, metadata-aware
- Metrics: precision, recall, F1, accuracy; 95% nonparametric bootstrap CI (3,000
  resamples) for recall and F1; local timing (200 repetitions, median/p95/mean)

## How to reproduce
```bash
pip install numpy
python3 src/run_experiment.py
python3 src/generate_charts.py
python3 src/generate_new_diagrams.py
```
Outputs:
- `results/raw_metrics.json` — full machine-readable metrics (confusion matrices,
  bootstrap CIs, timing, per-violation-type detection rates)
- `data/controlled_corpus.csv` — the generated 400-case corpus with ground truth
- `figures/*.png` — all 7 publication figures (5 data-driven + 2 conceptual
  diagrams), regenerated from the above

## Random seed
`SEED = 42` throughout (corpus shuffle and bootstrap resampling).

## What is synthetic vs. what is external fact
- **Synthetic / controlled (this study):** the entire 400-case corpus, all case
  labels, and all detector outputs. None of this represents real production
  data or real observed incidents.
- **External fact (cited, not measured):** the existence and mechanics of Delta
  Lake schema enforcement/evolution [1,2], the ODCS v3.2.0 specification [3,4],
  and the NYC TLC `cbd_congestion_fee` schema change [5,6] are used only as
  motivating, independently verifiable context — no NYC TLC trip records are
  used anywhere in the benchmark.

## Important limitations (see manuscript Section 8 for full discussion)
- This is a closed-world coverage benchmark, not a machine-learned classifier.
  A perfect (1.000) result for the metadata-aware detector is expected by
  construction and is not evidence of real-world predictive accuracy.
- Timing figures are local, single-machine, single-process Python measurements
  and are environment-sensitive (see `docs/environment.json`). They are not a
  production throughput or latency benchmark.
- The benchmark evaluates each violation type in isolation; compound/
  interacting violations are not modeled (see manuscript Section 10, Future Work).

## Independent reproduction record
`docs/REPRODUCTION_NOTE.md` documents a from-scratch re-implementation performed
during manuscript review, which reproduced identical confusion-matrix counts
and closely matching bootstrap intervals.

## Repository / DOI status
No public repository or DOI currently exists for this package. Before journal
submission, archive this package in a versioned public repository (e.g., GitHub)
and mint an archival DOI (e.g., via Zenodo); do not fabricate a DOI in the
interim.

## License
[Author to specify — e.g., MIT for code, CC-BY-4.0 for data/figures]
