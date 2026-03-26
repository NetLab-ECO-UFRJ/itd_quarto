#!/usr/bin/env python3
"""
Export summary heatmap tables as SVG files.

Generates the same heatmap tables shown in key-findings.qmd but as
standalone SVG files suitable for embedding in presentations, reports, etc.

Usage:
    python scripts/export_heatmap_svg.py                  # both UGC and Ads
    python scripts/export_heatmap_svg.py --scope ugc      # UGC only
    python scripts/export_heatmap_svg.py --scope ads      # Ads only
    python scripts/export_heatmap_svg.py -o output/       # custom output dir
"""

import argparse
import sys
from pathlib import Path

# Resolve project root
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from utils.summary_table import (
    scan_assessments,
    get_score_class,
    normalize_platform_name,
)

# Score band colors (background, text)
SCORE_COLORS = {
    'score-ideal':         ('#308BF2', '#143A66'),
    'score-satisfactory':  ('#43B5DF', '#1F5366'),
    'score-regular':       ('#F3CE49', '#66571F'),
    'score-precarious':    ('#F88C4A', '#663A1F'),
    'score-irrelevant':    ('#F64A9B', '#661F40'),
    'score-not-available': ('none', '#555555'),
    'score-missing':       ('#e0e0e0', '#666666'),
}

HEADER_BG = '#f8f9fa'
HEADER_FG = '#333333'
PLATFORM_BG = '#f8f9fa'
PLATFORM_FG = '#222222'

# Layout constants
COL_PLATFORM_W = 160
COL_SCORE_W = 100
ROW_H = 40
HEADER_H = 44
CELL_PAD = 4
CELL_RADIUS = 3
FONT_FAMILY = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
FONT_SIZE = 13
FONT_SIZE_HEADER = 13
REGIONS = ['BR', 'EU', 'UK']
REGION_LABELS = {'BR': 'Brazil', 'EU': 'EU', 'UK': 'UK'}


def _escape(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def generate_heatmap_svg(
    scope: str,
) -> str:
    """Generate an SVG string for the heatmap table."""
    scores = scan_assessments(project_root, scope)

    # Sort by average score descending
    def avg_score(regions_dict):
        vals = [v for v in regions_dict.values() if isinstance(v, (int, float))]
        return sum(vals) / len(vals) if vals else -1

    sorted_platforms = sorted(scores.items(), key=lambda x: avg_score(x[1]), reverse=True)

    num_rows = len(sorted_platforms)
    total_w = COL_PLATFORM_W + len(REGIONS) * COL_SCORE_W + (len(REGIONS)) * CELL_PAD + CELL_PAD
    total_h = HEADER_H + num_rows * (ROW_H + CELL_PAD) + CELL_PAD

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" '
        f'viewBox="0 0 {total_w} {total_h}" font-family="{FONT_FAMILY}">'
    )

    # Header row
    y = 0
    x = CELL_PAD
    parts.append(
        f'<rect x="{x}" y="{y}" width="{COL_PLATFORM_W}" height="{HEADER_H}" '
        f'rx="{CELL_RADIUS}" fill="{HEADER_BG}"/>'
    )
    parts.append(
        f'<text x="{x + 12}" y="{y + HEADER_H / 2 + 5}" font-size="{FONT_SIZE_HEADER}" '
        f'font-weight="600" fill="{HEADER_FG}">Platform</text>'
    )

    for i, region in enumerate(REGIONS):
        rx = CELL_PAD + COL_PLATFORM_W + CELL_PAD + i * (COL_SCORE_W + CELL_PAD)
        parts.append(
            f'<rect x="{rx}" y="{y}" width="{COL_SCORE_W}" height="{HEADER_H}" '
            f'rx="{CELL_RADIUS}" fill="{HEADER_BG}"/>'
        )
        parts.append(
            f'<text x="{rx + COL_SCORE_W / 2}" y="{y + HEADER_H / 2 + 5}" '
            f'font-size="{FONT_SIZE_HEADER}" font-weight="600" fill="{HEADER_FG}" '
            f'text-anchor="middle">{REGION_LABELS[region]}</text>'
        )

    # Data rows
    for row_idx, (platform, regions) in enumerate(sorted_platforms):
        y = HEADER_H + CELL_PAD + row_idx * (ROW_H + CELL_PAD)
        x = CELL_PAD

        # Platform name cell
        parts.append(
            f'<rect x="{x}" y="{y}" width="{COL_PLATFORM_W}" height="{ROW_H}" '
            f'rx="{CELL_RADIUS}" fill="{PLATFORM_BG}"/>'
        )
        parts.append(
            f'<text x="{x + 12}" y="{y + ROW_H / 2 + 5}" font-size="{FONT_SIZE}" '
            f'font-weight="600" fill="{PLATFORM_FG}">{_escape(platform)}</text>'
        )

        # Score cells
        for i, region in enumerate(REGIONS):
            rx = CELL_PAD + COL_PLATFORM_W + CELL_PAD + i * (COL_SCORE_W + CELL_PAD)
            score = regions.get(region)

            if score is None or score == 'N/A':
                bg, _ = SCORE_COLORS['score-missing']
            else:
                css_class = get_score_class(score)
                bg, _ = SCORE_COLORS[css_class]

            parts.append(
                f'<rect x="{rx}" y="{y}" width="{COL_SCORE_W}" height="{ROW_H}" '
                f'rx="{CELL_RADIUS}" fill="{bg}"/>'
            )

    parts.append('</svg>')
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser(description='Export heatmap tables as SVG')
    parser.add_argument(
        '--scope', choices=['ugc', 'ads', 'both'], default='both',
        help='Which assessment scope to export (default: both)'
    )
    parser.add_argument(
        '-o', '--output-dir', type=Path, default=project_root / 'output',
        help='Output directory (default: output/)'
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    scopes = ['ugc', 'ads'] if args.scope == 'both' else [args.scope]

    for scope in scopes:
        svg = generate_heatmap_svg(scope=scope)
        out_path = args.output_dir / f'heatmap_{scope}.svg'
        out_path.write_text(svg, encoding='utf-8')
        print(f'Exported: {out_path}')


if __name__ == '__main__':
    main()
