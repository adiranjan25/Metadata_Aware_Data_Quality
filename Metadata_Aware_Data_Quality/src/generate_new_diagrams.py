import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})

def box(ax, x, y, w, h, text, fc, ec, fontsize=9.3, textcolor="#1a1a1a", lw=1.5):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.02",
                        fc=fc, ec=ec, lw=lw, zorder=2)
    ax.add_patch(b)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fontsize, color=textcolor, zorder=3)

def line(ax, x1, y1, x2, y2, color="#888888", lw=1.3):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, zorder=1)

# ================= Figure 6: Violation taxonomy tree =================
fig, ax = plt.subplots(figsize=(11, 5.3))
ax.set_xlim(0, 11); ax.set_ylim(0, 5.3); ax.axis("off")
ax.text(5.5, 5.05, "Figure 6. Taxonomy of the Ten Injected Violation Classes",
        ha="center", fontsize=13, fontweight="bold")
ax.text(5.5, 4.7, "400-case controlled benchmark: 90 structural + 120 contract + 90 semantic/provenance + 100 clean controls",
        ha="center", fontsize=9, style="italic", color="#555555")

# Root
box(ax, 4.15, 3.85, 2.7, 0.6, "Controlled benchmark\n(400 cases)", fc="#EDEDED", ec="#333333", fontsize=9.8)

# Layer nodes
layer_defs = [
    ("Structural\n(90 cases)", "#2E5C8A", "#D6E8F5", 0.3, 2.6),
    ("Contract\n(120 cases)", "#B9770E", "#FCEBC9", 3.05, 2.9),
    ("Semantic / provenance\n(90 cases)", "#2E7D5B", "#D9EFE1", 6.10, 2.6),
]
for label, ec, fc, x, w in layer_defs:
    box(ax, x, 2.7, w, 0.6, label, fc=fc, ec=ec, fontsize=9.5, textcolor=ec)
    line(ax, 5.5, 3.85, x + w/2, 3.3, color="#999999")

# Clean-control node (separate branch)
box(ax, 8.85, 2.7, 1.7, 0.6, "Clean\n(100 cases)", fc="#F4F4F4", ec="#666666", fontsize=8.8, textcolor="#444444")
line(ax, 5.5, 3.85, 9.7, 3.3, color="#999999")

# Leaf classes per layer
structural_leaves = ["column\nadded\n(30)", "column\nremoved\n(30)", "type\nchanged\n(30)"]
contract_leaves = ["requiredness\nchanged\n(30)", "uniqueness\nchanged\n(30)", "range\nchanged\n(30)", "enum/domain\nchanged\n(30)"]
semantic_leaves = ["unit\nchanged\n(30)", "business\ndefinition\nchanged (30)", "lineage\nsource\nchanged (30)"]

def draw_leaves(leaves, parent_x, parent_w, ec, fc, y_top, fsize=None):
    n = len(leaves)
    total_w = parent_w
    leaf_w = total_w / n - 0.09
    if fsize is None:
        fsize = 8.8 if n <= 3 else 7.9
    xs = [parent_x + i * (leaf_w + 0.09) for i in range(n)]
    for x, lbl in zip(xs, leaves):
        box(ax, x, y_top, leaf_w, 1.05, lbl, fc=fc, ec=ec, fontsize=fsize, textcolor="#1a1a1a", lw=1.1)
        line(ax, parent_x + parent_w/2, 2.7, x + leaf_w/2, y_top + 1.05, color="#bbbbbb", lw=1.0)

draw_leaves(structural_leaves, 0.3, 2.6, "#2E5C8A", "#EAF1F8", 1.4)
draw_leaves(contract_leaves, 3.05, 2.9, "#B9770E", "#FDF3E0", 1.4)
draw_leaves(semantic_leaves, 6.10, 2.6, "#2E7D5B", "#E7F5EC", 1.4, fsize=7.6)

ax.text(5.5, 0.55, "Each leaf class contributes exactly 30 cases; detectors are evaluated per class in Figure 3.",
        ha="center", fontsize=9, color="#555555", style="italic")

plt.tight_layout()
plt.savefig("/home/claude/paper2/figures/fig6_taxonomy.png", dpi=230, bbox_inches="tight")
plt.close()

# ================= Figure 7: Nested detector-capability diagram =================
fig, ax = plt.subplots(figsize=(8.6, 7.4))
ax.set_xlim(-5.2, 5.2); ax.set_ylim(-5.7, 5.6); ax.axis("off")
ax.set_aspect("equal")
ax.text(0, 5.2, "Figure 7. Nested Detector Capability", ha="center", fontsize=13, fontweight="bold")
ax.text(0, 4.75, "Each detector's visible metadata is a strict superset of the one before it",
        ha="center", fontsize=9.2, style="italic", color="#555555")

circles = [
    (4.15, "#D9EFE1", "#2E7D5B", "Metadata-aware\n(schema + contract + semantic)\nrecall 1.000 / F1 1.000", 3.55),
    (3.05, "#FCEBC9", "#B9770E", "Contract-aware\n(schema + contract)\nrecall 0.700 / F1 0.824", 2.35),
    (1.85, "#D6E8F5", "#2E5C8A", "Schema-only\n(schema)\nrecall 0.300 / F1 0.462", 1.05),
]
for r, fc, ec, label, label_r in circles:
    c = Circle((0, -0.3), r, fc=fc, ec=ec, lw=2.0, alpha=0.85, zorder=1)
    ax.add_patch(c)

# labels placed within each ring's own annulus (verified by geometry so no
# label overlaps a smaller inner circle), alternating top/bottom for balance
ax.text(0, 3.05, "Metadata-aware\nschema + contract + semantic\nrecall 1.000  |  F1 1.000", ha="center", fontsize=8.3, color="#1d4d34", fontweight="bold")
ax.text(0, -0.3, "Schema-only\nschema\nrecall 0.300  |  F1 0.462", ha="center", fontsize=9.0, color="#1e3a5c", fontweight="bold")
ax.text(0, -2.8, "Contract-aware\nschema + contract\nrecall 0.700  |  F1 0.824", ha="center", fontsize=8.3, color="#7a5107", fontweight="bold")

ax.text(0, -5.35, "Concentric by design: the benchmark defines each wider detector as inheriting every rule of the narrower ones,\nso recall and F1 increase monotonically from inner to outer circle (Table 1, Figure 5).",
        ha="center", fontsize=8.6, color="#555555", style="italic")

plt.tight_layout()
plt.savefig("/home/claude/paper2/figures/fig7_capability_nesting.png", dpi=230, bbox_inches="tight")
plt.close()

print("Figures 6 and 7 generated.")
