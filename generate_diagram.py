"""Run this script once to generate architecture.png"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(16, 11))
ax.set_xlim(0, 16)
ax.set_ylim(0, 11)
ax.axis("off")
fig.patch.set_facecolor("#F0F4F8")

BLUE_DARK  = "#1F4E79"
BLUE_MID   = "#2E75B6"
BLUE_LIGHT = "#BDD7EE"
GREEN      = "#375623"
GREEN_LIGHT= "#E2EFDA"
ORANGE     = "#C55A11"
ORANGE_LT  = "#FCE4D6"
PURPLE     = "#4B0082"
PURPLE_LT  = "#EDE7F6"
GREY       = "#595959"
COPILOT    = "#6E40C9"
COPILOT_LT = "#F0EBFF"
WHITE      = "#FFFFFF"

def box(ax, x, y, w, h, label, sublabel="", bg=WHITE, border=BLUE_DARK, fontsize=10):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                          facecolor=bg, edgecolor=border, linewidth=1.8, zorder=3)
    ax.add_patch(rect)
    cy = y + h / 2 + (0.15 if sublabel else 0)
    ax.text(x + w / 2, cy, label, ha="center", va="center",
            fontsize=fontsize, fontweight="bold", color=border, zorder=4)
    if sublabel:
        ax.text(x + w / 2, y + h / 2 - 0.22, sublabel, ha="center", va="center",
                fontsize=7.5, color=GREY, zorder=4)

def arrow(ax, x1, y1, x2, y2, color=BLUE_DARK):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.8), zorder=5)

def copilot_badge(ax, x, y, label):
    rect = FancyBboxPatch((x, y), 2.6, 0.55, boxstyle="round,pad=0.06",
                          facecolor=COPILOT_LT, edgecolor=COPILOT, linewidth=1.4, zorder=6)
    ax.add_patch(rect)
    ax.text(x + 1.3, y + 0.275, f"✦ Copilot: {label}", ha="center", va="center",
            fontsize=7.2, color=COPILOT, fontweight="bold", zorder=7)

# ── Title ──────────────────────────────────────────────────────────────────────
ax.text(8, 10.5, "FinDoc Extractor — System Architecture",
        ha="center", va="center", fontsize=15, fontweight="bold", color=BLUE_DARK)
ax.text(8, 10.1, "Microsoft Agents League @ AI Skills Fest 2026 · Track 1: Creative Apps (GitHub Copilot)",
        ha="center", va="center", fontsize=9, color=GREY)

# ── Row 1: User Input ──────────────────────────────────────────────────────────
box(ax, 0.4, 8.2, 3.2, 1.2, "User", "SEC Filing\n(PDF / HTML)",
    bg="#E8F5E9", border="#2E7D32", fontsize=10)

box(ax, 5.0, 8.2, 3.2, 1.2, "Streamlit UI", "File upload · Results display\nDownload button",
    bg=BLUE_LIGHT, border=BLUE_DARK, fontsize=10)

box(ax, 9.8, 8.2, 3.2, 1.2, "Document Parser", "pdfplumber (PDF)\nBeautifulSoup (HTML)",
    bg=ORANGE_LT, border=ORANGE, fontsize=10)

box(ax, 12.5, 8.2, 3.1, 1.2, "Plain Text\nExtract", "~50,000–200,000\nchars",
    bg="#F9F9F9", border=GREY, fontsize=9)

# Row 1 arrows
arrow(ax, 3.6, 8.8, 5.0, 8.8)
arrow(ax, 8.2, 8.8, 9.8, 8.8)
arrow(ax, 13.0, 8.2, 13.0, 7.6)

# Copilot badges row 1
copilot_badge(ax, 9.9, 9.55, "parse_pdf / parse_html")

# ── Row 2: LLM Extraction ──────────────────────────────────────────────────────
box(ax, 5.0, 6.2, 3.2, 1.2, "LLM Extractor", "Azure OpenAI GPT-4o\nor GitHub Models (free)",
    bg=PURPLE_LT, border=PURPLE, fontsize=10)

box(ax, 9.8, 6.2, 3.2, 1.2, "Extracted Metrics", "14 fields: revenue, EPS,\nEBITDA, debt, audit…",
    bg="#F9F9F9", border=GREY, fontsize=9)

# Row 2 arrows
arrow(ax, 6.6, 8.2, 6.6, 7.4)
arrow(ax, 13.0, 7.6, 11.4, 6.9)   # text → LLM
arrow(ax, 8.2, 6.8, 9.8, 6.8)

# Copilot badges row 2
copilot_badge(ax, 5.1, 7.55, "prompt template + schema")

# ── Row 3: Anomaly + Export ────────────────────────────────────────────────────
box(ax, 2.0, 4.1, 3.2, 1.2, "Anomaly Detector", "6 rule-based flags\nRevenue · D/E · Audit…",
    bg=ORANGE_LT, border=ORANGE, fontsize=10)

box(ax, 7.0, 4.1, 3.2, 1.2, "Excel Exporter", "3 sheets: Summary,\nAnomaly Flags, Raw",
    bg=GREEN_LIGHT, border=GREEN, fontsize=10)

box(ax, 12.0, 4.1, 3.2, 1.2, "Excel Report\n(.xlsx)", "Color-coded severity\nFormatted headers",
    bg="#E8F5E9", border="#2E7D32", fontsize=9)

# Row 3 arrows
arrow(ax, 9.8, 6.5, 3.6, 5.3)    # metrics → anomaly
arrow(ax, 9.8, 6.5, 8.6, 5.3)    # metrics → excel
arrow(ax, 5.2, 4.7, 7.0, 4.7)    # anomaly → excel
arrow(ax, 10.2, 4.7, 12.0, 4.7)  # excel → file

# Copilot badges row 3
copilot_badge(ax, 2.1, 5.45, "anomaly rule functions")
copilot_badge(ax, 7.1, 5.45, "openpyxl formatting code")

# ── GitHub Copilot Legend ──────────────────────────────────────────────────────
legend_x, legend_y = 0.4, 2.7
rect = FancyBboxPatch((legend_x, legend_y - 0.1), 15.2, 1.6,
                      boxstyle="round,pad=0.1", facecolor=COPILOT_LT,
                      edgecolor=COPILOT, linewidth=1.6, zorder=2)
ax.add_patch(rect)
ax.text(8, legend_y + 1.25, "GitHub Copilot Contributions",
        ha="center", fontsize=10, fontweight="bold", color=COPILOT)

copilot_items = [
    (0.8,  legend_y + 0.6,  "parse_pdf & parse_html\ngenerated from docstrings"),
    (4.2,  legend_y + 0.6,  "LLM prompt template\ngenerated from schema dict"),
    (7.6,  legend_y + 0.6,  "Anomaly rules\nfrom inline comments"),
    (11.0, legend_y + 0.6,  "Excel cell formatting\nfrom function signature"),
]
for cx, cy, txt in copilot_items:
    ax.text(cx + 1.2, cy, txt, ha="center", va="center",
            fontsize=8, color=PURPLE, bbox=dict(boxstyle="round,pad=0.3",
            facecolor=WHITE, edgecolor=COPILOT, linewidth=1.0))

# ── Footer ─────────────────────────────────────────────────────────────────────
ax.text(8, 0.3, "Built with GitHub Copilot · Streamlit · pdfplumber · Azure OpenAI GPT-4o · openpyxl",
        ha="center", fontsize=8, color=GREY, style="italic")

plt.tight_layout(pad=0.5)
plt.savefig("architecture.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("architecture.png saved.")
