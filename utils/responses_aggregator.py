"""
Aggregates responses across all platforms for comparison views.
"""

import yaml
import markdown
from pathlib import Path
from typing import Dict, Any, List
from collections import OrderedDict

PROJECT_ROOT = Path(__file__).parent.parent


def get_all_platforms(year: str = "2025") -> List[Dict[str, Any]]:
    """Get all platform directories with their metadata."""
    platforms = []

    global_dir = PROJECT_ROOT / "data" / year / "global"
    if global_dir.exists():
        for platform_dir in sorted(global_dir.iterdir()):
            if platform_dir.is_dir():
                platforms.append({
                    "name": platform_dir.name.title(),
                    "path": platform_dir,
                    "scope": "Global",
                    "region": None
                })

    regional_dir = PROJECT_ROOT / "data" / year / "regional"
    if regional_dir.exists():
        for region_dir in sorted(regional_dir.iterdir()):
            if region_dir.is_dir():
                for platform_dir in sorted(region_dir.iterdir()):
                    if platform_dir.is_dir():
                        platforms.append({
                            "name": platform_dir.name.title(),
                            "path": platform_dir,
                            "scope": "Regional",
                            "region": region_dir.name
                        })

    return platforms


def load_questions_ordered(year: str = "2025", question_type: str = "ugc") -> OrderedDict:
    """Load questions preserving category order."""
    filename = f"questions_{question_type}_{year}.yml"
    filepath = PROJECT_ROOT / "data" / year / filename

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


def get_answer_icon(answer_label: str) -> str:
    """Get icon for answer value."""
    label_lower = answer_label.lower() if answer_label else ""
    if label_lower in ["yes", "full", "both"]:
        return "✅"
    elif label_lower in ["partial", "yes, but only for approved researchers"]:
        return "⚠️"
    elif label_lower in ["no", "no or not applicable"]:
        return "❌"
    elif label_lower in ["not applicable"]:
        return "➖"
    elif "api" in label_lower or "gui" in label_lower:
        return "🔧"
    return ""


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
