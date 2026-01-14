#!/usr/bin/env python3
"""Reorder answers in YAML files to match question definition order."""

import yaml
from pathlib import Path


def get_question_order(questions_file: Path) -> dict[str, int]:
    """Extract question code order from questions file."""
    with open(questions_file, 'r') as f:
        data = yaml.safe_load(f)

    order = {}
    idx = 0
    for category, questions in data.items():
        if isinstance(questions, list):
            for q in questions:
                order[q['code']] = idx
                idx += 1
    return order


def fix_answer_order(answers_file: Path, question_order: dict[str, int]):
    """Reorder answers in a YAML file to match question order."""
    with open(answers_file, 'r') as f:
        data = yaml.safe_load(f)

    for key, value in data.items():
        if key.endswith('_answers') and isinstance(value, list):
            data[key] = sorted(value, key=lambda x: question_order.get(x['code'], 999))

    with open(answers_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    project_root = Path(__file__).parent.parent

    # Fix UGC files
    ugc_order = get_question_order(project_root / 'data/2025/questions_ugc_2025.yml')
    for ugc_file in project_root.glob('data/2025/**/ugc.yml'):
        print(f"Fixing {ugc_file}")
        fix_answer_order(ugc_file, ugc_order)

    # Fix ADS files
    ads_order = get_question_order(project_root / 'data/2025/questions_ads_2025.yml')
    for ads_file in project_root.glob('data/2025/**/ads.yml'):
        print(f"Fixing {ads_file}")
        fix_answer_order(ads_file, ads_order)


if __name__ == '__main__':
    main()
