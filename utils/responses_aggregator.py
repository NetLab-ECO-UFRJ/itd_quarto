"""
Aggregates responses across all platforms for comparison views.
"""

import yaml
import markdown
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from collections import OrderedDict
from .quarto_helpers import get_answer_icon, get_platform_sources

PROJECT_ROOT = Path(__file__).parent.parent


def _get_data_root(year: str) -> Path:
    """Resolve data root for flat and legacy layouts."""
    flat_root = PROJECT_ROOT / "data"
    legacy_root = PROJECT_ROOT / "data" / year

    if (flat_root / "global").exists() or (flat_root / "regional").exists():
        return flat_root
    if legacy_root.exists():
        return legacy_root
    return flat_root


def _resolve_question_file(year: str, question_type: str) -> Path:
    """Resolve questions file path for flat and legacy layouts."""
    filename = f"questions_{question_type}_{year}.yml"
    data_root = _get_data_root(year)
    candidates = [
        data_root / filename,
        PROJECT_ROOT / "data" / year / filename,
    ]
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


EXCLUDED_SLUGS = {"meta"}


def get_all_platforms(year: str = "2025") -> List[Dict[str, Any]]:
    """Get all platform directories with their metadata."""
    platforms = []

    data_root = _get_data_root(year)
    global_dir = data_root / "global"
    if global_dir.exists():
        for platform_dir in sorted(global_dir.iterdir()):
            if platform_dir.is_dir() and platform_dir.name not in EXCLUDED_SLUGS:
                platforms.append({
                    "name": platform_dir.name.title(),
                    "path": platform_dir,
                    "scope": "Global",
                    "region": None
                })

    regional_dir = data_root / "regional"
    if regional_dir.exists():
        for region_dir in sorted(regional_dir.iterdir()):
            if region_dir.is_dir():
                for platform_dir in sorted(region_dir.iterdir()):
                    if platform_dir.is_dir() and platform_dir.name not in EXCLUDED_SLUGS:
                        platforms.append({
                            "name": platform_dir.name.title(),
                            "path": platform_dir,
                            "scope": "Regional",
                            "region": region_dir.name
                        })

    return platforms


def get_available_regions(year: str = "2025") -> List[str]:
    """Get sorted region codes available under data/regional."""
    regional_dir = _get_data_root(year) / "regional"
    if not regional_dir.exists():
        return []
    return sorted([p.name for p in regional_dir.iterdir() if p.is_dir()])


def get_available_platforms(year: str = "2025") -> List[str]:
    """Get sorted unique platform slugs across global and regional scopes."""
    platforms = set()
    data_root = _get_data_root(year)
    global_dir = data_root / "global"
    if global_dir.exists():
        for platform_dir in global_dir.iterdir():
            if platform_dir.is_dir():
                platforms.add(platform_dir.name)
    regional_dir = data_root / "regional"
    if regional_dir.exists():
        for region_dir in regional_dir.iterdir():
            if region_dir.is_dir():
                for platform_dir in region_dir.iterdir():
                    if platform_dir.is_dir():
                        platforms.add(platform_dir.name)
    return sorted(platforms)


def load_questions_ordered(year: str = "2025", question_type: str = "ugc") -> OrderedDict:
    """Load questions preserving category order."""
    filepath = _resolve_question_file(year, question_type)

    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    questions = OrderedDict()
    for category_name, questions_list in data.items():
        if isinstance(questions_list, list):
            category_label = category_name.replace('-', ' ').replace('_', ' ').title()
            questions[category_name] = {
                "label": category_label,
                "questions": []
            }
            for q in questions_list:
                questions[category_name]["questions"].append({
                    "code": q["code"],
                    "title": q.get("title", ""),
                    "answers": {a["value"]: a["label"] for a in q.get("answers", [])}
                })

    return questions


def load_platform_answers(platform_path: Path, question_type: str) -> Dict[str, Any]:
    """Load answers for a single platform."""
    answers_file = platform_path / f"{question_type}.yml"
    if not answers_file.exists():
        return {}

    with open(answers_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    answers_by_code = {}
    for key, value in data.items():
        if key.endswith("_answers") and isinstance(value, list):
            for answer in value:
                code = answer.get("code")
                if code:
                    answers_by_code[code] = {
                        "selected_answer": answer.get("selected_answer", ""),
                        "notes": answer.get("notes") or ""
                    }

    return answers_by_code


def load_platform_answers_from_file(filepath: Path) -> Dict[str, Any]:
    """Load answers from a full YAML file path."""
    if not filepath.exists():
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    answers_by_code = {}
    for key, value in data.items():
        if key.endswith("_answers") and isinstance(value, list):
            for answer in value:
                code = answer.get("code")
                if code:
                    answers_by_code[code] = {
                        "selected_answer": answer.get("selected_answer", ""),
                        "notes": answer.get("notes") or ""
                    }
    return answers_by_code


def load_platform_answers_by_region(
    platform: str,
    year: str = "2025",
    question_type: str = "ugc",
    regions: Optional[List[str]] = None,
    include_global: bool = True,
) -> Dict[str, Dict[str, Any]]:
    """Load answers for a platform across regions and optional global scope."""
    answers_by_region: Dict[str, Dict[str, Any]] = {}
    data_root = _get_data_root(year)

    if include_global:
        global_path = data_root / "global" / platform
        answers_by_region["GLOBAL"] = load_platform_answers(global_path, question_type)

    regions_list = regions if regions is not None else get_available_regions(year)
    for region in regions_list:
        regional_path = data_root / "regional" / region / platform
        answers_by_region[region] = load_platform_answers(regional_path, question_type)

    return answers_by_region


def get_platform_coverage(
    platform: str,
    year: str = "2025",
    question_type: str = "ugc",
    regions: Optional[List[str]] = None,
) -> Tuple[bool, List[str]]:
    """Return (has_global, region_list_with_data) for the given platform and question type."""
    data_root = _get_data_root(year)
    has_global = (data_root / "global" / platform / f"{question_type}.yml").exists()
    regions_list = regions if regions is not None else get_available_regions(year)
    regions_with_data = []
    for region in regions_list:
        regional_file = data_root / "regional" / region / platform / f"{question_type}.yml"
        if regional_file.exists():
            regions_with_data.append(region)
    return has_global, regions_with_data


def aggregate_responses(year: str = "2025", question_type: str = "ugc") -> Dict[str, Any]:
    """
    Aggregate all responses across platforms, organized by question.

    Returns:
        {
            "categories": OrderedDict of {
                "category_name": {
                    "label": "Category Label",
                    "questions": [
                        {
                            "code": "UGC_SC1",
                            "title": "Question text",
                            "responses": [
                                {
                                    "platform": "Bluesky",
                                    "scope": "Global",
                                    "region": None,
                                    "answer_value": "yes",
                                    "answer_label": "Yes",
                                    "notes": "Justification text"
                                },
                                ...
                            ]
                        }
                    ]
                }
            }
        }
    """
    questions = load_questions_ordered(year, question_type)
    platforms = get_all_platforms(year)

    platform_answers = {}
    for p in platforms:
        key = f"{p['name']}_{p['region'] or 'global'}"
        platform_answers[key] = {
            "meta": p,
            "answers": load_platform_answers(p["path"], question_type)
        }

    result = {"categories": OrderedDict()}

    for cat_name, cat_data in questions.items():
        result["categories"][cat_name] = {
            "label": cat_data["label"],
            "questions": []
        }

        for q in cat_data["questions"]:
            question_entry = {
                "code": q["code"],
                "title": q["title"],
                "responses": []
            }

            for key, pdata in platform_answers.items():
                meta = pdata["meta"]
                answers = pdata["answers"]

                answer_data = answers.get(q["code"], {})
                answer_value = answer_data.get("selected_answer", "")
                answer_label = q["answers"].get(answer_value, answer_value) if answer_value else ""
                if answer_label == "not_applicable":
                    answer_label = "Not Applicable"

                question_entry["responses"].append({
                    "platform": meta["name"],
                    "scope": meta["scope"],
                    "region": meta["region"],
                    "answer_value": answer_value,
                    "answer_label": answer_label,
                    "notes": answer_data.get("notes", "")
                })

            result["categories"][cat_name]["questions"].append(question_entry)

    return result


def _classify_answer(label: str) -> str:
    l = (label or "").lower().strip()
    if not l:
        return "empty"
    if l.startswith("yes") or l in ["full", "both"] or l.startswith("free"):
        return "yes"
    if l == "no" or l == "no or not applicable":
        return "no"
    if "partial" in l:
        return "partial"
    if "not applicable" in l:
        return "na"
    if "api" in l or "gui" in l:
        return "partial"
    return "no"


def generate_responses_summary(question_type: str = "ugc", year: str = "2025"):
    """Generate visual summary with stat cards and stacked bar chart."""
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

    data = aggregate_responses(year, question_type)

    cat_stats = OrderedDict()
    total_yes = 0
    total_answered = 0
    total_platforms = set()

    for cat_name, cat_data in data["categories"].items():
        yes = 0; no = 0; partial = 0; na = 0
        for q in cat_data["questions"]:
            for r in q["responses"]:
                total_platforms.add(r["platform"])
                cls = _classify_answer(r["answer_label"])
                if cls == "yes": yes += 1
                elif cls == "no": no += 1
                elif cls == "partial": partial += 1
                elif cls == "na": na += 1
        answered = yes + no + partial + na
        cat_stats[cat_data["label"]] = {
            "yes": yes, "no": no, "partial": partial, "na": na,
            "total": answered,
        }
        total_yes += yes + partial
        total_answered += answered

    overall_rate = round(100 * total_yes / total_answered) if total_answered else 0

    best_cat = max(cat_stats.items(), key=lambda x: (x[1]["yes"] + x[1]["partial"]) / x[1]["total"] if x[1]["total"] else 0)
    worst_cat = min(cat_stats.items(), key=lambda x: (x[1]["yes"] + x[1]["partial"]) / x[1]["total"] if x[1]["total"] else 1)

    framework = "UGC" if question_type == "ugc" else "Advertising"

    print(f"""
```{{=html}}
<div style="display: flex; gap: 16px; margin: 20px 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 160px; border-radius: 8px; padding: 16px 20px; background: #f8f9fa; border: 1px solid #e0e0e0; text-align: center;">
    <div style="font-size: 2rem; font-weight: 700; color: {'#1b9e77' if overall_rate > 50 else '#d95f02'};">{overall_rate}%</div>
    <div style="font-size: 0.85rem; color: #666;">Overall Positive Rate</div>
  </div>
  <div style="flex: 1; min-width: 160px; border-radius: 8px; padding: 16px 20px; background: #f8f9fa; border: 1px solid #e0e0e0; text-align: center;">
    <div style="font-size: 1.1rem; font-weight: 700; color: #1b9e77;">{best_cat[0]}</div>
    <div style="font-size: 0.85rem; color: #666;">Strongest Category</div>
  </div>
  <div style="flex: 1; min-width: 160px; border-radius: 8px; padding: 16px 20px; background: #f8f9fa; border: 1px solid #e0e0e0; text-align: center;">
    <div style="font-size: 1.1rem; font-weight: 700; color: #d95f02;">{worst_cat[0]}</div>
    <div style="font-size: 0.85rem; color: #666;">Weakest Category</div>
  </div>
</div>
```
""")

    categories = list(cat_stats.keys())
    yes_vals = [cat_stats[c]["yes"] for c in categories]
    partial_vals = [cat_stats[c]["partial"] for c in categories]
    no_vals = [cat_stats[c]["no"] for c in categories]
    na_vals = [cat_stats[c]["na"] for c in categories]
    totals = [cat_stats[c]["total"] for c in categories]

    yes_pct = [100 * v / t if t else 0 for v, t in zip(yes_vals, totals)]
    partial_pct = [100 * v / t if t else 0 for v, t in zip(partial_vals, totals)]
    no_pct = [100 * v / t if t else 0 for v, t in zip(no_vals, totals)]
    na_pct = [100 * v / t if t else 0 for v, t in zip(na_vals, totals)]

    y = np.arange(len(categories))
    bar_h = 0.6

    fig, ax = plt.subplots(figsize=(8, max(2.5, len(categories) * 0.55)))

    left = np.zeros(len(categories))
    ax.barh(y, yes_pct, bar_h, left=left, color='#1b9e77', label='Yes', zorder=3)
    left += yes_pct
    ax.barh(y, partial_pct, bar_h, left=left, color='#66c2a5', label='Partial', zorder=3)
    left += partial_pct
    ax.barh(y, no_pct, bar_h, left=left, color='#d95f02', label='No', zorder=3)
    left += no_pct
    if any(v > 0 for v in na_pct):
        ax.barh(y, na_pct, bar_h, left=left, color='#cccccc', label='N/A', zorder=3)

    for i, cat in enumerate(categories):
        t = totals[i]
        y_count = yes_vals[i] + partial_vals[i]
        ax.text(101, i, f'{y_count}/{t}', va='center', ha='left', fontsize=8, color='#555')

    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=9)
    ax.set_xlim(0, 115)
    ax.set_xlabel('% of Assessed Responses', fontsize=9)
    ax.set_title(f'{framework} — Answer Distribution by Category', fontsize=11, fontweight='600', pad=25)
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=4, fontsize=8, framealpha=0.9)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])

    plt.tight_layout()
    plt.show()
    plt.close(fig)


def get_answer_sort_order(answer_label: str) -> int:
    """Get sort order for answer (best answers first)."""
    label_lower = answer_label.lower() if answer_label else ""
    if label_lower in ["yes", "full", "both"]:
        return 0
    elif label_lower in ["partial", "yes, but only for approved researchers"]:
        return 1
    elif "api" in label_lower or "gui" in label_lower:
        return 2
    elif label_lower in ["not applicable"]:
        return 3
    elif label_lower in ["no", "no or not applicable"]:
        return 4
    elif not label_lower:
        return 5
    return 3


def generate_responses_by_question(question_type: str = "ugc", year: str = "2025"):
    """Generate HTML tables showing all responses per question."""
    data = aggregate_responses(year, question_type)

    for cat_name, cat_data in data["categories"].items():
        print(f"\n## {cat_data['label']}\n")

        for q in cat_data["questions"]:
            print(f"\n### {q['code']}: {q['title']}\n")
            print('```{=html}')
            print('<div style="max-width:900px;">')
            print('<table style="width:100%; table-layout:fixed; border-collapse:collapse; font-size:0.9em;">')
            print('<colgroup>')
            print('<col style="width:140px;">')
            print('<col style="width:120px;">')
            print('<col style="width:auto;">')
            print('</colgroup>')
            print('<thead>')
            print('<tr style="border-bottom:2px solid #ddd;">')
            print('<th style="text-align:left; padding:8px;">Platform</th>')
            print('<th style="text-align:left; padding:8px;">Response</th>')
            print('<th style="text-align:left; padding:8px;">Justification</th>')
            print('</tr>')
            print('</thead>')
            print('<tbody>')

            sorted_responses = sorted(q["responses"], key=lambda r: (get_answer_sort_order(r["answer_label"]), r["platform"]))

            for resp in sorted_responses:
                platform_name = resp["platform"]
                if resp["region"]:
                    platform_name = f"{resp['platform']} ({resp['region']})"

                icon = get_answer_icon(resp["answer_label"])
                answer_display = f"{icon} {resp['answer_label']}" if resp["answer_label"] else "—"

                notes_text = (resp["notes"] or "").replace('\n', ' ').replace('\r', ' ')
                if not notes_text or notes_text == "-":
                    notes = "—"
                else:
                    notes = markdown.markdown(notes_text, extensions=['extra'])

                print('<tr style="border-bottom:1px solid #eee;">')
                print(f'<td style="padding:8px; vertical-align:top;"><strong>{platform_name}</strong></td>')
                print(f'<td style="padding:8px; vertical-align:top;">{answer_display}</td>')
                print(f'<td style="padding:8px; vertical-align:top; word-wrap:break-word; overflow-wrap:break-word;">{notes}</td>')
                print('</tr>')

            print('</tbody>')
            print('</table>')
            print('</div>')
            print('```\n')


def generate_platform_question_sections(
    platform: str,
    question_type: str = "ugc",
    year: str = "2025",
    heading_level: int = 3,
):
    """Generate per-question sections for a single platform with region rows.

    Reads the `sources` frontmatter from the platform's appendix QMD to
    determine which YAML file to load for each region.
    """
    questions = load_questions_ordered(year, question_type)

    sources = get_platform_sources(platform, question_type, PROJECT_ROOT)
    if not sources:
        print("\n**Coverage:** Not assessed\n")
        return

    answers_by_region: Dict[str, Dict[str, Any]] = {}
    for region, filepath in sources.items():
        answers_by_region[region] = load_platform_answers_from_file(PROJECT_ROOT / filepath)

    display_regions = list(sources.keys())
    coverage_label = ", ".join(display_regions)
    print(f"\n**Coverage:** {coverage_label}\n")

    cat_h = "#" * heading_level
    q_h = "#" * (heading_level + 1)

    for cat_data in questions.values():
        print(f"\n{cat_h} {cat_data['label']}\n")
        for q in cat_data["questions"]:
            print(f"\n{q_h} {q['code']}: {q['title']}\n")
            print('```{=html}')
            print('<table style="width:100% !important; table-layout:fixed; border-collapse:collapse; font-size:0.9em;">')
            print('<colgroup>')
            print('<col style="width:120px;">')
            print('<col style="width:160px;">')
            print('<col style="width:auto;">')
            print('</colgroup>')
            print('<thead>')
            print('<tr style="border-bottom:2px solid #ddd;">')
            print('<th style="text-align:left; padding:8px; width:120px;">Region</th>')
            print('<th style="text-align:left; padding:8px; width:160px;">Answer</th>')
            print('<th style="text-align:left; padding:8px;">Note</th>')
            print('</tr>')
            print('</thead>')
            print('<tbody>')

            for region in display_regions:
                answer_data = answers_by_region.get(region, {}).get(q["code"], {})
                answer_value = (answer_data.get("selected_answer") or "").strip()
                if not answer_value:
                    answer_label = "Not assessed"
                elif answer_value in ["not_applicable", "not applicable"]:
                    answer_label = "Not applicable"
                else:
                    answer_label = q["answers"].get(answer_value, answer_value)

                answer_icon = get_answer_icon(answer_label)
                if answer_icon:
                    answer_icon += " "

                notes_text = (answer_data.get("notes") or "").replace('\n', ' ').replace('\r', ' ')
                if not notes_text or notes_text == "-":
                    notes = "-"
                else:
                    notes = markdown.markdown(notes_text, extensions=['extra'])

                print('<tr style="border-bottom:1px solid #eee;">')
                print(f'<td style="padding:8px; vertical-align:top; width:120px;"><strong>{region}</strong></td>')
                print(f'<td style="padding:8px; vertical-align:top; width:160px;">{answer_icon}{answer_label}</td>')
                print(f'<td style="padding:8px; vertical-align:top; word-wrap:break-word; overflow-wrap:break-word;">{notes}</td>')
                print('</tr>')

            print('</tbody>')
            print('</table>')
            print('```\n')
