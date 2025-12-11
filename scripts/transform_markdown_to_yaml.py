#!/usr/bin/env python3
"""
Transform Markdown assessment responses to YAML format.

This script reads Markdown files containing platform assessment responses
and generates YAML files in the required format for each platform and scope.
"""

import re
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional


class MarkdownToYAMLTransformer:
    ANSWER_MAPPINGS = {
        'ads': {
            'yes, with full availability': 'full',
            'yes, with partial availability': 'partial',
            'yes, through the gui': 'gui',
            'yes, through the api': 'api',
            'yes, the api documentation': 'api',
            'yes, the gui documentation': 'gui',
            'free api access': 'api',
            'free gui access': 'gui',
            'yes': 'yes',
            'no or not applicable': 'not_applicable',
            'not applicable': 'not_applicable',
            'no': 'no',
        },
        'ugc': {
            'yes, but only for approved researchers': 'researchers_only',
            'yes': 'yes',
            'no or not applicable': 'no_or_not_applicable',
            'not applicable': 'not_applicable',
            'no': 'no',
        }
    }

    def __init__(self, base_dir: Path, scope_type: str = "global", region_code: Optional[str] = None):
        self.base_dir = base_dir
        self.markdown_dir = base_dir / "data" / "2025" / "doc_backups"
        self.scope_type = scope_type.lower()
        self.region_code = region_code.upper() if region_code else None

        if self.scope_type == "global":
            self.output_dir = base_dir / "data" / "2025" / "global"
        elif self.scope_type == "regional" and self.region_code:
            self.output_dir = base_dir / "data" / "2025" / "regional" / self.region_code
        else:
            raise ValueError("For regional scope, region_code must be provided")

        questions_dir = base_dir / "data" / "2025"
        self.questions_ads = self._load_yaml(questions_dir / "questions_ads_2025.yml")
        self.questions_ugc = self._load_yaml(questions_dir / "questions_ugc_2025.yml")

    def _load_yaml(self, filepath: Path) -> Dict:
        """Load YAML file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _normalize_answer(self, answer_text: str, scope: str) -> str:
        """Normalize answer values from markdown text to YAML answer options."""
        if not answer_text:
            return "no"

        answer_lower = answer_text.strip().lower()
        mappings = self.ANSWER_MAPPINGS.get(scope.lower(), {})

        for pattern, value in mappings.items():
            if pattern in answer_lower:
                return value

        return "no"

    def _get_full_code(self, code: str, scope: str) -> str:
        """Add scope prefix to question code."""
        prefix = "AD" if scope.lower() == "ads" else "UGC"
        return code if code.startswith(f"{prefix}_") else f"{prefix}_{code}"

    def _categorize_question(self, code: str, scope: str) -> str:
        """Determine which category a question belongs to."""
        questions = self.questions_ads if scope.lower() == "ads" else self.questions_ugc
        full_code = self._get_full_code(code, scope)

        for category_name, category_questions in questions.items():
            if isinstance(category_questions, list):
                for q in category_questions:
                    if q.get('code') == full_code:
                        return category_name

        return "special_criteria" if code.startswith("SC") else "accessibility"

    def _extract_notes(self, question_content: str) -> str:
        """Extract notes from question content."""
        bullet_items = list(re.finditer(r'-\s+[^\n]+', question_content))
        if not bullet_items:
            return ""

        text_after_bullets = question_content[bullet_items[-1].end():].strip()
        notes_pattern = r'^([^\-\#\*][^\n]*(?:\n(?![^\S\n]*(?:\-|\#\#\#|\*\*[A-Z]+\d+:|OTHER CRITERIA|SPECIAL CRITERIA))[^\n]*)*)'
        notes_match = re.match(notes_pattern, text_after_bullets, re.MULTILINE)

        if notes_match:
            return self._clean_markdown_text(notes_match.group(1).strip())
        return ""

    def _extract_questions_and_answers(self, content: str, scope: str) -> List[Dict]:
        """Parse markdown to extract Q&A pairs."""
        questions = []
        question_pattern = r'\*\*([A-Z]+\d+):\s*([^\*]+?)\*\*'
        matches = list(re.finditer(question_pattern, content, re.MULTILINE))

        for i, match in enumerate(matches):
            code = match.group(1)
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            question_content = content[start_pos:end_pos]

            answer_pattern = r'-\s+\*\*(.+?)\*\*'
            selected_answers = re.findall(answer_pattern, question_content)

            if not selected_answers:
                normalized_answer = "no"
                notes = ""
            else:
                normalized_answers = []
                for answer in selected_answers:
                    normalized = self._normalize_answer(answer, scope)
                    if normalized not in normalized_answers:
                        normalized_answers.append(normalized)

                if len(normalized_answers) > 1 and "api" in normalized_answers:
                    normalized_answer = "api"
                else:
                    normalized_answer = normalized_answers[0]

                notes = self._extract_notes(question_content)

            questions.append({
                'code': self._get_full_code(code, scope),
                'selected_answer': normalized_answer,
                'notes': notes
            })

        return questions

    def _clean_markdown_text(self, text: str) -> str:
        """Clean markdown formatting from text while preserving content."""
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
        text = re.sub(r'_{2,}([^_]+)_{2,}', r'\1', text)
        return text.strip()

    def parse_markdown_file(self, markdown_path: Path, evaluation_date: str) -> Dict:
        """Parse markdown file and extract assessment data."""
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        filename = markdown_path.stem
        parts = filename.split('_')

        if len(parts) < 3:
            raise ValueError(f"Invalid filename format: {filename}. Expected format: region_SCOPE_platform.md")

        region, scope = parts[0].upper(), parts[1].upper()
        platform = '_'.join(parts[2:]).lower()

        qa_pairs = self._extract_questions_and_answers(content, scope)

        answers_by_category = {}
        for qa in qa_pairs:
            code = qa['code'].replace('AD_', '').replace('UGC_', '')
            category = self._categorize_question(code, scope)

            if category not in answers_by_category:
                answers_by_category[category] = []
            answers_by_category[category].append(qa)

        for category in answers_by_category:
            answers_by_category[category].sort(key=lambda x: x['code'])

        return {
            'platform': platform,
            'region_code': region,
            'scope': scope,
            'evaluation_date': evaluation_date,
            'answers_by_category': answers_by_category
        }

    def _generate_yaml_content(self, assessment: Dict) -> Dict:
        """Generate YAML structure for an assessment."""
        yaml_data = {
            'metadata': {
                'platform': assessment['platform'].capitalize(),
                'region_code': assessment['region_code'],
                'scope': assessment['scope'],
                'evaluation_date': assessment['evaluation_date']
            }
        }

        for category, answers in assessment['answers_by_category'].items():
            key = f"{category.replace('_', '-')}_answers"
            yaml_data[key] = answers

        return yaml_data

    def _write_yaml_file(self, platform: str, scope: str, yaml_data: Dict):
        """Write YAML data to file with proper formatting."""
        platform_dir = self.output_dir / platform
        platform_dir.mkdir(parents=True, exist_ok=True)

        output_file = platform_dir / f"{scope.lower()}.yml"

        class QuotedString(str):
            pass

        yaml.add_representer(
            QuotedString,
            lambda dumper, data: dumper.represent_scalar('tag:yaml.org,2002:str', data, style="'")
        )

        for category_key, category_data in yaml_data.items():
            if isinstance(category_data, list):
                for answer in category_data:
                    if 'selected_answer' in answer:
                        value = answer['selected_answer']
                        if value in ['yes', 'no', 'not_applicable']:
                            answer['selected_answer'] = QuotedString(value)

        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"✓ Created: {output_file}")

    def transform(self, markdown_file: str, evaluation_date: str):
        """Process markdown file and generate YAML output."""
        print("Starting transformation...\n")

        markdown_path = self.markdown_dir / markdown_file
        if not markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

        print(f"Processing: {markdown_path.name}")
        assessment = self.parse_markdown_file(markdown_path, evaluation_date)

        yaml_data = self._generate_yaml_content(assessment)
        self._write_yaml_file(assessment['platform'], assessment['scope'], yaml_data)

        print(f"  Processed {assessment['scope']} assessment for {assessment['platform']}\n")
        print("Transformation complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Transform Markdown assessment responses to YAML format"
    )
    parser.add_argument(
        "--markdown-file",
        required=True,
        help="Markdown filename in doc_backups/markdown (e.g., eu_ADS_Meta.md)"
    )
    parser.add_argument(
        "--scope-type",
        choices=["global", "regional"],
        default="regional",
        help="Scope type: global or regional (default: regional)"
    )
    parser.add_argument(
        "--region",
        help="Region code (required for regional scope, e.g., BR, EU, UK)"
    )
    parser.add_argument(
        "--evaluation-date",
        required=True,
        help="Evaluation date in YYYY-MM format (e.g., 2025-11)"
    )

    args = parser.parse_args()

    if args.scope_type == "regional" and not args.region:
        parser.error("--region is required when --scope-type is regional")

    base_dir = Path(__file__).parent.parent
    transformer = MarkdownToYAMLTransformer(
        base_dir,
        scope_type=args.scope_type,
        region_code=args.region
    )
    transformer.transform(
        markdown_file=args.markdown_file,
        evaluation_date=args.evaluation_date
    )


if __name__ == "__main__":
    main()
