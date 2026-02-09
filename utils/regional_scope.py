"""
Generate a table of source links in appendix frontmatter.

Shows all mappings for UGC and Ads, with paths shortened by removing
the leading data/2025 prefix.
"""

from pathlib import Path
from typing import Dict, List
import html

from .quarto_helpers import parse_qmd_frontmatter


def _shorten_path(path: str) -> str:
    prefix = "data/2025/"
    return path[len(prefix):] if path.startswith(prefix) else path


def generate_unexpected_links_table() -> str:
    """
    Build an HTML table showing all links in appendix sources.

    Uses chapters/appendices/*.qmd frontmatter (sources.ugc / sources.ads).
    """
    project_root = Path.cwd()
    while not (project_root / "utils").exists() and project_root != project_root.parent:
        project_root = project_root.parent

    appendices_dir = project_root / "chapters" / "appendices"
    if not appendices_dir.exists():
        return "<p><em>No appendices found.</em></p>"

    rows = []
    for qmd_path in sorted(appendices_dir.glob("*.qmd")):
        frontmatter = parse_qmd_frontmatter(qmd_path)
        title = frontmatter.get("title") or qmd_path.stem
        sources = frontmatter.get("sources", {}) or {}
        ugc_map = sources.get("ugc", {}) or {}
        ads_map = sources.get("ads", {}) or {}

        def format_map(mapping: Dict[str, str]) -> List[str]:
            if not mapping:
                return []
            keys = list(mapping.keys())
            # Prefer GLOBAL first, then alphabetical
            ordered = (["GLOBAL"] if "GLOBAL" in mapping else []) + sorted(
                [k for k in keys if k != "GLOBAL"]
            )
            items: List[str] = []
            for region in ordered:
                path = mapping.get(region)
                if not isinstance(path, str):
                    continue
                items.append(f"{region}: {_shorten_path(path)}")
            return items

        ugc_items = format_map(ugc_map)
        ads_items = format_map(ads_map)

        rows.append({
            "platform": title,
            "ugc": ugc_items,
            "ads": ads_items,
        })

    def cell(items: List[str]) -> str:
        if not items:
            return "—"
        return "<br>".join(html.escape(item) for item in items)

    html_table = """
<table class="unexpected-links-table">
  <thead>
    <tr>
      <th>Platform</th>
      <th>UGC links</th>
      <th>Ads links</th>
    </tr>
  </thead>
  <tbody>
"""
    for row in rows:
        html_table += "    <tr>\n"
        html_table += f"      <td>{html.escape(str(row['platform']))}</td>\n"
        html_table += f"      <td>{cell(row['ugc'])}</td>\n"
        html_table += f"      <td>{cell(row['ads'])}</td>\n"
        html_table += "    </tr>\n"

    html_table += "  </tbody>\n</table>\n"
    html_table += """
<style>
.unexpected-links-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-family: system-ui, -apple-system, sans-serif;
}
.unexpected-links-table th,
.unexpected-links-table td {
  border: 1px solid #ddd;
  padding: 8px 10px;
  vertical-align: top;
}
.unexpected-links-table th {
  background: #f8f9fa;
  text-align: left;
}
</style>
"""
    return html_table
