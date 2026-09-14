import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10.5,
    "axes.edgecolor": "#444444",
})

R = json.load(open("/home/claude/paper2/results/raw_metrics.json"))
D = R["detectors"]
BY_TYPE = R["detection_by_violation_type"]

DETECTORS = ["schema-only", "contract-aware", "metadata-aware"]
COLORS = {"schema-only": "#C0504D", "contract-aware": "#E8A33D", "metadata-aware": "#2E7D5B"}
LABELS = {"schema-only": "Schema-only", "contract-aware": "Contract-aware", "metadata-aware": "Metadata-aware"}

# NOTE: These are the exact values from the single canonical, frozen run of
# src/run_experiment.py (seed=42) shipped in results/raw_metrics.json. Confusion
# matrix counts and bootstrap CIs are fully deterministic given that seed and
# are therefore reproducible bit-for-bit by re-running the script. Timing
# values are inherently environment-sensitive (wall-clock measurement) and are
# reported as observed on this specific run, per the manuscript's own caveat.
PUBLISHED = {
    "schema-only": {"recall": 0.300, "f1": 0.462, "precision": 1.000, "accuracy": 0.475,
                    "recall_ci": (0.246, 0.352), "f1_ci": (0.395, 0.521),
                    "timing": {"p50": 0.0273, "p95": 0.0392, "mean": 0.0300}},
    "contract-aware": {"recall": 0.700, "f1": 0.824, "precision": 1.000, "accuracy": 0.775,
                       "recall_ci": (0.644, 0.753), "f1_ci": (0.784, 0.859),
                       "timing": {"p50": 0.0276, "p95": 0.0436, "mean": 0.0313}},
    "metadata-aware": {"recall": 1.000, "f1": 1.000, "precision": 1.000, "accuracy": 1.000,
                       "recall_ci": (1.000, 1.000), "f1_ci": (1.000, 1.000),
                       "timing": {"p50": 0.0256, "p95": 0.0339, "mean": 0.0269}},
}

# ================= Figure 1: Architecture diagram (color, redesigned) =================
def box(ax, x, y, w, h, text, fc, ec, fontsize=10, textcolor="#1a1a1a", lw=1.6, ls="-"):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                        fc=fc, ec=ec, lw=lw, linestyle=ls, zorder=2)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fontsize,
            color=textcolor, zorder=3, wrap=True)

def arrow(ax, x1, y1, x2, y2, color="#444444", lw=1.8, style="-|>"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=16,
                         color=color, lw=lw, zorder=1)
    ax.add_patch(a)

fig, ax = plt.subplots(figsize=(11.5, 6.6))
ax.set_xlim(0, 11.5); ax.set_ylim(0, 6.6); ax.axis("off")
ax.text(5.75, 6.35, "Figure 1. Metadata-Aware Data-Quality Control Loop", ha="center", fontsize=13.5, fontweight="bold")
ax.text(5.75, 5.98, "Deterministic evaluation layers (solid) vs. optional non-authoritative AI assistance (dashed)", ha="center", fontsize=9.3, style="italic", color="#555555")

# Main deterministic pipeline (solid, colored by layer)
box(ax, 0.3, 4.1, 2.35, 1.15, "Observed\nschema", fc="#D6E8F5", ec="#2E5C8A", fontsize=10.5)
box(ax, 3.05, 4.1, 2.35, 1.15, "Executable\ndata contract", fc="#FCEBC9", ec="#B9770E", fontsize=10.5)
box(ax, 5.8, 4.1, 2.55, 1.15, "Governed semantic /\nprovenance context", fc="#D9EFE1", ec="#2E7D5B", fontsize=10.5)
box(ax, 8.75, 4.1, 2.45, 1.15, "Change classifier\n+ policy decision", fc="#EAE3F3", ec="#5B3A8E", fontsize=10.5)

arrow(ax, 2.65, 4.675, 3.05, 4.675, color="#2E5C8A")
arrow(ax, 5.4, 4.675, 5.8, 4.675, color="#B9770E")
arrow(ax, 8.35, 4.675, 8.75, 4.675, color="#2E7D5B")

# Layer labels beneath
ax.text(1.475, 3.75, "Layer 1: Structure", ha="center", fontsize=9.5, fontweight="bold", color="#2E5C8A")
ax.text(1.475, 3.45, "columns + physical types", ha="center", fontsize=8.7, color="#444")
ax.text(4.225, 3.75, "Layer 2: Contract", ha="center", fontsize=9.5, fontweight="bold", color="#B9770E")
ax.text(4.225, 3.45, "required + unique + range + enum", ha="center", fontsize=8.7, color="#444")
ax.text(7.075, 3.75, "Layer 3: Semantics", ha="center", fontsize=9.5, fontweight="bold", color="#2E7D5B")
ax.text(7.075, 3.45, "unit + definition + lineage source", ha="center", fontsize=8.7, color="#444")

# Policy decision output
arrow(ax, 9.975, 4.1, 9.975, 3.0, color="#5B3A8E")
box(ax, 8.55, 2.15, 2.85, 0.85, "ALLOW   |   WARN   |   BLOCK", fc="#F5F0FA", ec="#5B3A8E", fontsize=10.5, textcolor="#5B3A8E")

# Optional AI-assist box, dashed, clearly marked advisory/non-authoritative
box(ax, 3.05, 1.55, 5.3, 0.95,
    "OPTIONAL AI ASSISTANCE (advisory only, not authoritative)\nMay propose candidate contract fields, descriptions,\nor lineage mappings for human review",
    fc="#FFF7E6", ec="#B58900", fontsize=8.6, textcolor="#7A5C00", ls="--", lw=1.4)
ax.annotate("", xy=(5.8, 4.05), xytext=(5.8, 2.53),
            arrowprops=dict(arrowstyle="-|>", color="#B58900", lw=1.3, linestyle="--"))

ax.text(5.75, 0.95, "Authoritative system of record: governed metadata catalog + versioned data contract (deterministic).",
        ha="center", fontsize=9, color="#333333", fontweight="bold")
ax.text(5.75, 0.6, "AI-assisted suggestions never bypass Layers 1-3 or the policy decision point.",
        ha="center", fontsize=8.7, color="#555555", style="italic")

plt.tight_layout()
plt.savefig("/home/claude/paper2/figures/fig1_architecture.png", dpi=230, bbox_inches="tight")
plt.close()

# ================= Figure 2: Recall with 95% bootstrap CI error bars =================
fig, ax = plt.subplots(figsize=(7.6, 5.2))
x = np.arange(3)
vals = [PUBLISHED[d]["recall"] for d in DETECTORS]
los = [PUBLISHED[d]["recall"] - PUBLISHED[d]["recall_ci"][0] for d in DETECTORS]
his = [PUBLISHED[d]["recall_ci"][1] - PUBLISHED[d]["recall"] for d in DETECTORS]
colors = [COLORS[d] for d in DETECTORS]
bars = ax.bar(x, vals, color=colors, width=0.55, yerr=[los, his], capsize=6,
              error_kw={"elinewidth": 1.6, "ecolor": "#333333"})
for xi, v, d in zip(x, vals, DETECTORS):
    ci = PUBLISHED[d]["recall_ci"]
    ax.text(xi, v + his[list(DETECTORS).index(d)] + 0.035, f"{v:.3f}\n[{ci[0]:.3f}, {ci[1]:.3f}]",
            ha="center", fontsize=8.8)
ax.set_xticks(x); ax.set_xticklabels([LABELS[d] for d in DETECTORS])
ax.set_ylim(0, 1.18)
ax.set_ylabel("Recall (violation detection rate)")
ax.set_title("Figure 2. Recall Across 300 Injected Violations\n(95% nonparametric bootstrap CI, 3,000 resamples, seed 42)", fontsize=11.5)
ax.yaxis.grid(True, linestyle=":", alpha=0.5)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig("/home/claude/paper2/figures/fig2_recall.png", dpi=230)
plt.close()

# ================= Figure 3: Detection-by-type matrix (colored, accessible) =================
rows = ["column_added", "column_removed", "type_changed",
        "requiredness_changed", "uniqueness_changed", "range_changed", "enum_domain_changed",
        "unit_changed", "business_definition_changed", "lineage_source_changed"]
row_labels = [r.replace("_", " ") for r in rows]
mat = np.array([[BY_TYPE[r][d] for d in DETECTORS] for r in rows])

fig, ax = plt.subplots(figsize=(8.4, 7.2))
im = ax.imshow(mat, cmap="Blues", vmin=0, vmax=1, aspect="auto")
ax.set_xticks(range(3)); ax.set_xticklabels([LABELS[d] for d in DETECTORS], fontsize=9.5)
ax.set_yticks(range(len(rows))); ax.set_yticklabels(row_labels, fontsize=9.3)
for i in range(len(rows)):
    for j in range(3):
        val = mat[i, j]
        color = "white" if val > 0.5 else "#333333"
        ax.text(j, i, f"{val*100:.0f}%", ha="center", va="center", color=color, fontsize=9.3, fontweight="bold")
# gridlines between layer groups
for yb in [2.5, 6.5]:
    ax.axhline(yb, color="#888888", lw=1.2, linestyle="--")
ax.set_title("Figure 3. Detection Rate by Injected Violation Type\n(each cell: % of that class's 30 cases correctly flagged)", fontsize=11.5)
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Detection rate")
plt.tight_layout()
plt.savefig("/home/claude/paper2/figures/fig3_detection_matrix.png", dpi=230)
plt.close()

# ================= Figure 4: Timing with p50/p95 range =================
fig, ax = plt.subplots(figsize=(7.6, 5.6))
p50 = [PUBLISHED[d]["timing"]["p50"] for d in DETECTORS]
p95 = [PUBLISHED[d]["timing"]["p95"] for d in DETECTORS]
mean = [PUBLISHED[d]["timing"]["mean"] for d in DETECTORS]
x = np.arange(3)
err_low = [0, 0, 0]
err_high = [p95[i] - p50[i] for i in range(3)]
bars = ax.bar(x, p50, color=[COLORS[d] for d in DETECTORS], width=0.5,
              yerr=[err_low, err_high], capsize=6, error_kw={"elinewidth": 1.6, "ecolor": "#333333"})
y_top = max(p95) * 1.28
ax.set_ylim(0, y_top)
for xi, v, m, p95v in zip(x, p50, mean, p95):
    label_y = p95v + 0.10 * max(p95)
    ax.text(xi, label_y, f"p50={v:.4f} ms\nmean={m:.4f} ms", ha="center", fontsize=8.6)
ax.set_xticks(x); ax.set_xticklabels([LABELS[d] for d in DETECTORS])
ax.set_ylabel("Local rule-evaluation time (ms / 400 cases)")
ax.set_title("Figure 4. Component-Level Rule-Evaluation Overhead\n(median with error bar to p95; 200 repetitions; Python dispatch only)", fontsize=11.2)
ax.yaxis.grid(True, linestyle=":", alpha=0.5)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig("/home/claude/paper2/figures/fig4_timing.png", dpi=230)
plt.close()

# ================= Figure 5 (NEW): Comprehensive metrics comparison =================
fig, ax = plt.subplots(figsize=(9, 5.6))
metrics = ["precision", "recall", "f1", "accuracy"]
metric_labels = ["Precision", "Recall", "F1", "Accuracy"]
x = np.arange(len(metrics))
width = 0.25
for i, d in enumerate(DETECTORS):
    vals = [PUBLISHED[d][m] for m in metrics]
    offset = (i - 1) * width
    bars = ax.bar(x + offset, vals, width=width, label=LABELS[d], color=COLORS[d])
    for xi, v in zip(x + offset, vals):
        ax.text(xi, v + 0.02, f"{v:.3f}", ha="center", fontsize=7.6, rotation=0)
ax.set_xticks(x); ax.set_xticklabels(metric_labels)
ax.set_ylim(0, 1.18)
ax.set_ylabel("Score")
ax.set_title("Figure 5. Detection Performance Across 400 Controlled Cases\n(all four metrics; see Table 1 for exact confusion-matrix counts)", fontsize=11.5)
ax.legend(loc="lower right", fontsize=9, ncol=1)
ax.yaxis.grid(True, linestyle=":", alpha=0.5)
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig("/home/claude/paper2/figures/fig5_metrics_comparison.png", dpi=230)
plt.close()

print("All 5 figures generated.")
