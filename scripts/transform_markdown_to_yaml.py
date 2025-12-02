#!/usr/bin/env python3
"""
Transform Markdown assessment responses to YAML format.

This script reads Markdown files containing platform assessment responses
and generates YAML files in the required format for each platform and scope.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse


class MarkdownToYAMLTransformer:
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

        self.questions_dir = base_dir / "data" / "2025"
        self.template_dir = base_dir / "templates"

        self.questions_ads = self._load_questions("questions_ads_2025.yml")
        self.questions_ugc = self._load_questions("questions_ugc_2025.yml")

    def _load_questions(self, filename: str) -> Dict:
        """Load question definitions from YAML."""
        filepath = self.questions_dir / filename
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _normalize_answer_from_markdown(self, answer_text: str, scope: str) -> str:
        """
        Normalize answer values from markdown text to YAML answer options.
        """
        if not answer_text:
            return "no"

        answer_lower = answer_text.strip().lower()

        # ADS scope mappings
        if scope.lower() == "ads":
            if "yes, with full availability" in answer_lower:
                return "full"
            elif "yes, with partial availability" in answer_lower:
                return "partial"
            elif "yes, through the gui" in answer_lower:
                return "gui"
            elif "yes, through the api" in answer_lower:
                return "api"
            elif "yes, the api documentation" in answer_lower:
                return "api"
            elif "yes, the gui documentation" in answer_lower:
                return "gui"
            elif "free api access" in answer_lower:
                return "api"
            elif "free gui access" in answer_lower:
                return "gui"
            elif answer_lower == "yes":
                return "yes"
            elif "no or not applicable" in answer_lower:
                return "no_or_not_applicable"
            elif "not applicable" in answer_lower:
                return "not_applicable"
            elif answer_lower == "no":
                return "no"
            else:
                return "no"

        # UGC scope mappings
        elif scope.lower() == "ugc":
            if "yes, but only for approved researchers" in answer_lower:
                return "researchers_only"
            elif answer_lower == "yes":
                return "yes"
            elif "not applicable" in answer_lower:
                return "not_applicable"
            elif answer_lower == "no":
                return "no"
            else:
                return "no"

        return "no"

    def _extract_question_code(self, question_header: str) -> Optional[str]:
        """Extract question code (e.g., SC1, OC1) from question header."""
        match = re.search(r'\*\*([A-Z]+\d+):', question_header)
        return match.group(1) if match else None

    def _categorize_question(self, code: str, scope: str) -> str:
        """Determine which category a question belongs to."""
        questions = self.questions_ads if scope.lower() == "ads" else self.questions_ugc

        # Add prefix based on scope
        if scope.lower() == 'ads':
            full_code = f"AD_{code}" if not code.startswith("AD_") else code
        else:
            full_code = f"UGC_{code}" if not code.startswith("UGC_") else code

        for category_name, category_questions in questions.items():
            if isinstance(category_questions, list):
                for q in category_questions:
                    if q.get('code') == full_code:
                        return category_name

        # Fallback based on code prefix
        if code.startswith("SC"):
            return "special_criteria"
        elif code.startswith("OC"):
            return "accessibility"

        return "accessibility"

    def _extract_questions_and_answers(self, content: str, scope: str) -> List[Dict]:
        """Parse markdown to extract Q&A pairs."""
        questions = []

        # Split content by question headers (bold text with question codes)
        # Pattern: **SC1:** or **OC15:**
        question_pattern = r'\*\*([A-Z]+\d+):\s*([^\*]+?)\*\*'

        matches = list(re.finditer(question_pattern, content, re.MULTILINE))

        for i, match in enumerate(matches):
            code = match.group(1)

            # Get content from this question to the next question (or end of file)
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            question_content = content[start_pos:end_pos]

            # Extract selected answer(s) - look for bold answers in bullet list
            # Pattern: -   **answer text**
            answer_pattern = r'-\s+\*\*(.+?)\*\*'
            selected_answers = re.findall(answer_pattern, question_content)

            if not selected_answers:
                # No answer selected, use default
                normalized_answer = "no"
                notes = ""
            else:
                # Normalize each selected answer
                normalized_answers = []
                for answer in selected_answers:
                    normalized = self._normalize_answer_from_markdown(answer, scope)
                    if normalized not in normalized_answers:
                        normalized_answers.append(normalized)

                # Combine multiple answers if both GUI and API are selected
                if len(normalized_answers) > 1:
                    # Sort to ensure consistent ordering
                    normalized_answers.sort()
                    if "api" in normalized_answers and "gui" in normalized_answers:
                        normalized_answer = "api"  # Take first one based on existing pattern
                    else:
                        normalized_answer = normalized_answers[0]
                else:
                    normalized_answer = normalized_answers[0]

                # Extract notes - text after the answer list, but before next section/question
                # Find all bullet items (answers)
                bullet_items = list(re.finditer(r'-\s+[^\n]+', question_content))

                if bullet_items:
                    # Get text after the last bullet item
                    last_bullet = bullet_items[-1]
                    text_after_bullets = question_content[last_bullet.end():].strip()

                    # Extract only plain text paragraphs (not starting with -, #, *, or uppercase section headers)
                    # Stop at next question, section header, or end
                    notes_match = re.match(r'^([^\-\#\*][^\n]*(?:\n(?![^\S\n]*(?:\-|\#\#\#|\*\*[A-Z]+\d+:|OTHER CRITERIA|SPECIAL CRITERIA))[^\n]*)*)',
                                         text_after_bullets, re.MULTILINE)
                    if notes_match:
                        notes = notes_match.group(1).strip()
                        # Clean up markdown formatting
                        notes = self._clean_markdown_text(notes) if notes else ""
                    else:
                        notes = ""
                else:
                    notes = ""

            # Add prefix based on scope
            if scope.lower() == 'ads':
                full_code = f"AD_{code}"
            else:
                full_code = f"UGC_{code}"

            questions.append({
                'code': full_code,
                'selected_answer': normalized_answer,
                'notes': notes
            })

        return questions

    def _clean_markdown_text(self, text: str) -> str:
        """Clean markdown formatting from text while preserving content."""
        # Remove extra whitespace and newlines
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        # Remove markdown links but keep the text
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

        # Remove bold markers
        text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)

        # Remove underline markers
        text = re.sub(r'_{2,}([^_]+)_{2,}', r'\1', text)

        return text.strip()

    def parse_markdown_file(self, markdown_path: Path, evaluation_date: str) -> Dict:
        """Parse markdown file and extract assessment data."""
        # Read markdown content
        with open(markdown_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata from filename
        # Format: {region}_{scope}_{platform}.md
        filename = markdown_path.stem
        parts = filename.split('_')

        if len(parts) < 3:
            raise ValueError(f"Invalid filename format: {filename}. Expected format: region_SCOPE_platform.md")

        region = parts[0].upper()
        scope = parts[1].upper()
        platform = '_'.join(parts[2:]).lower()

        # Extract questions and answers
        qa_pairs = self._extract_questions_and_answers(content, scope)

        # Group by category
        answers_by_category = {}
        for qa in qa_pairs:
            code = qa['code'].replace('AD_', '').replace('UGC_', '')
            category = self._categorize_question(code, scope)

            if category not in answers_by_category:
                answers_by_category[category] = []

            answers_by_category[category].append(qa)

        # Sort answers within each category by code
        for category in answers_by_category:
            answers_by_category[category] = sorted(
                answers_by_category[category],
                key=lambda x: x['code']
            )

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
            # Convert underscores to hyphens in category name for YAML keys
            category_with_hyphens = category.replace('_', '-')
            key = f"{category_with_hyphens}_answers"
            yaml_data[key] = answers

        return yaml_data

    def _write_yaml_file(self, platform: str, scope: str, yaml_data: Dict):
        """Write YAML data to file."""
        platform_dir = self.output_dir / platform
        platform_dir.mkdir(parents=True, exist_ok=True)

        output_file = platform_dir / f"{scope.lower()}.yml"

        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"✓ Created: {output_file}")

    def _create_qmd_from_template(self, platform: str) -> bool:
        """
        Create QMD file from template if both ads.yml and ugc.yml exist.
        Returns True if QMD was created, False otherwise.
        """
        platform_dir = self.output_dir / platform
        ads_file = platform_dir / "ads.yml"
        ugc_file = platform_dir / "ugc.yml"

        if not ads_file.exists() or not ugc_file.exists():
            return False

        template_file = self.template_dir / "platform_template.qmd"
        if not template_file.exists():
            print(f"⚠ Warning: Template file not found: {template_file}")
            return False

        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()

        platform_title = platform.capitalize()

        if self.scope_type == "regional":
            platform_path = f"data/2025/regional/{self.region_code}/{platform}"
        else:
            platform_path = f"data/2025/global/{platform}"

        qmd_content = template_content.replace("data/2025/global/{PLATFORM_NAME}", platform_path)
        qmd_content = qmd_content.replace("{PLATFORM_TITLE}", platform_title)

        output_file = platform_dir / f"{platform}.qmd"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(qmd_content)

        print(f"✓ Created QMD: {output_file}")
        return True

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

        print("\nChecking if QMD file can be generated...")
        if self._create_qmd_from_template(assessment['platform']):
            print("✓ QMD file created")
        else:
            print("  Skipped QMD: missing ads.yml or ugc.yml")

        print("\nTransformation complete!")


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
