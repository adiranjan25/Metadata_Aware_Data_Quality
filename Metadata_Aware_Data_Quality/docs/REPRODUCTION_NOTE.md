# Reproducibility Note

**Script:** `src/run_experiment.py` (seed = 42)
**Status:** This note documents the single canonical, frozen execution of the
benchmark script whose output (`results/raw_metrics.json`) is what the
manuscript's Table 1, Table 3, and Figures 2-5 report directly. Every number
printed in the manuscript for this experiment was copied from this file —
there is no separate "manuscript" version of the numbers that differs from
what ships in this package.

## What is fully deterministic (verified by running the script twice)

The confusion-matrix counts and the 95% bootstrap confidence intervals were
confirmed bit-for-bit identical across two independent executions of
`run_experiment.py`:

| Detector | TP | FP | FN | TN | Precision | Recall | F1 | Accuracy |
|---|---|---|---|---|---|---|---|---|
| Schema-only | 90 | 0 | 210 | 100 | 1.000 | 0.300 | 0.462 | 0.475 |
| Contract-aware | 210 | 0 | 90 | 100 | 1.000 | 0.700 | 0.824 | 0.775 |
| Metadata-aware | 300 | 0 | 0 | 100 | 1.000 | 1.000 | 1.000 | 1.000 |

| Detector | Recall 95% CI | F1 95% CI |
|---|---|---|
| Schema-only | [0.246, 0.352] | [0.395, 0.521] |
| Contract-aware | [0.644, 0.753] | [0.784, 0.859] |
| Metadata-aware | [1.000, 1.000] | [1.000, 1.000] |

This determinism is expected: given a fixed random seed, the corpus
construction, shuffle order, and bootstrap resampling are all fully specified
by `SEED = 42`, so re-running the unmodified script reproduces these values
exactly, on any machine, every time.

## What is not deterministic, and is reported as observed

Component-level timing (Table 3, Figure 4) measures real wall-clock elapsed
time for 200 repetitions of rule dispatch per detector. This is inherently
sensitive to CPU load, scheduling, and the host environment, and will differ
between runs and between machines even with the same seed. The values in
Table 3 (p50/p95/mean in milliseconds) are those observed on the specific run
whose full output is stored in `results/raw_metrics.json` in this package;
re-running the script on a different machine will produce different absolute
numbers of the same order of magnitude (tens of microseconds per 400 cases).
This is explicitly flagged as a limitation in the manuscript (Sections 5.3
and 8) and should not be read as a production latency benchmark.

## How to verify this yourself

```bash
pip install numpy
python3 src/run_experiment.py
```
Compare the printed confusion-matrix and CI values against Table 1 and the
text of Section 6 — they should match exactly. Timing values will differ from
Table 3 by a small amount; this is expected and documented above.
