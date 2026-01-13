#!/usr/bin/env python3
"""
Transform Excel assessment responses to YAML format.

This script reads Excel files containing platform assessment responses
and generates YAML files in the required format for each platform and scope.
"""

import pandas as pd
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import re
import argparse


class ExcelToYAMLTransformer:
    def __init__(self, base_dir: Path, scope_type: str = "global", region_code: Optional[str] = None):
        self.base_dir = base_dir
        self.xlsx_dir = base_dir / "data" / "2025" / "xlsx_backups"
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

    def _normalize_answer(self, raw_answer: str, question_code: str, scope: str) -> str:
        """
        Normalize answer values based on question definition.
        Maps Excel responses to YAML answer options.
        """
        if pd.isna(raw_answer) or raw_answer == "":
            return "no"

        raw_lower = str(raw_answer).strip().lower()

        questions = self.questions_ads if scope == "ads" else self.questions_ugc

        question_def = self._find_question_definition(question_code, questions)
        if not question_def:
            if "yes" in raw_lower:
                return "yes"
            elif "partial" in raw_lower:
                return "partial"
            else:
                return "no"

        answer_options = question_def.get('answers', {})
        if isinstance(answer_options, list):
            available_options = [opt.get('value', '') for opt in answer_options]
        else:
            available_options = list(answer_options.keys()) if answer_options else []

        # Priority 1: Check for "partial" keyword BEFORE checking for "full"
        # This prevents "Yes, with partial availability" from matching "full"
        if "partial" in available_options and "partial" in raw_lower:
            return "partial"

        # Priority 2: Check for "full" keyword
        if "full" in available_options:
            if "full" in raw_lower:
                return "full"
            # If only "yes" (not "full" or "partial"), map to "full" if that's expected
            if raw_lower == "yes" and "yes" not in available_options:
                return "full"

        # Priority 3: Check for API/GUI specific answers
        # First check if BOTH gui and api are mentioned
        has_gui = ("free gui" in raw_lower or "through the gui" in raw_lower or
                   "gui documentation" in raw_lower or raw_lower == "gui")
        has_api = ("free api" in raw_lower or "through the api" in raw_lower or
                   "api documentation" in raw_lower or raw_lower == "api")

        if has_gui and has_api and "both" in available_options:
            return "both"

        # Then check for individual values
        if "api" in available_options and has_api:
            return "api"

        if "gui" in available_options and has_gui:
            return "gui"

        # Priority 4: Check for yes/no answers
        if "yes" in available_options:
            if "yes" in raw_lower:
                return "yes"
            elif "no" in raw_lower:
                if "no" in available_options:
                    return "no"
                else:
                    return "no_or_not_applicable"
            else:
                return "no_or_not_applicable"

        # Priority 5: Check for "no" answer
        if "no" in available_options and ("no" in raw_lower or raw_lower == "no"):
            return "no"

        # Priority 6: Check for "no_or_not_applicable" answer
        if "no_or_not_applicable" in available_options:
            if "no or not applicable" in raw_lower or "not applicable" in raw_lower:
                return "no_or_not_applicable"

        # Priority 7: Check for "not_applicable" answer
        if "not_applicable" in available_options:
            if "not applicable" in raw_lower:
                return "not_applicable"

        # Default fallback
        if "no_or_not_applicable" in available_options:
            return "no_or_not_applicable"
        elif "no" in available_options:
            return "no"
        else:
            return "no"

    def _find_question_definition(self, code: str, questions: Dict) -> Dict:
        """Find question definition by code."""
        for category in questions.values():
            if isinstance(category, list):
                for q in category:
                    if q.get('code') == code:
                        return q
        return {}

    def _extract_question_code(self, column_name: str) -> str:
        """Extract question code (e.g., SC1, OC1) from column header."""
        match = re.search(r'\b(SC\d+|OC\d+)\b', column_name)
        return match.group(1) if match else None

    def _categorize_question(self, code: str, scope: str) -> str:
        """Determine which category a question belongs to."""
        questions = self.questions_ads if scope == "ads" else self.questions_ugc

        # Use AD_ for ads scope, UGC_ for ugc scope
        if scope.lower() == 'ads':
            full_code = f"AD_{code}" if not code.startswith("AD_") else code
        else:
            full_code = f"{scope.upper()}_{code}" if not code.startswith(scope.upper()) else code

        for category_name, category_questions in questions.items():
            if isinstance(category_questions, list):
                for q in category_questions:
                    if q.get('code') == full_code:
                        return category_name

        if code.startswith("SC"):
            return "special_criteria"
        elif code.startswith("OC"):
            return "accessibility"

        return "accessibility"

    def _process_excel_file(self, excel_path: Path, scope: str) -> List[Dict]:
        """Process a single Excel file and return list of assessments."""
        df = pd.read_excel(excel_path)

        assessments = []

        for idx, row in df.iterrows():
            platform = row.get('Which platform is being analyzed?')
            region = row.get('Which region is being analyzed?')
            timestamp = row.get('Carimbo de data/hora')
            analysts = row.get('Identification of analysts')

            if pd.isna(platform) or platform == "":
                continue

            platform_clean = str(platform).strip().lower().replace('/', '_').replace(' ', '_')
            region_code = str(region).strip().upper() if not pd.isna(region) else "BR"

            eval_date = None
            if not pd.isna(timestamp):
                try:
                    dt = pd.to_datetime(timestamp)
                    eval_date = dt.strftime("%Y-%m")
                except:
                    eval_date = "2025-11"
            else:
                eval_date = "2025-11"

            answers_by_category = {}

            for col in df.columns:
                if 'Justification' in col or 'Notes' in col:
                    continue

                question_code = self._extract_question_code(col)
                if not question_code:
                    continue

                answer_value = row[col]

                justification_col = None
                for next_col in df.columns:
                    if question_code in next_col and ('Justification' in next_col or 'Notes' in next_col):
                        justification_col = next_col
                        break

                justification = ""
                if justification_col:
                    just_val = row[justification_col]
                    justification = str(just_val) if not pd.isna(just_val) else ""

                # Use AD_ for ads scope, UGC_ for ugc scope
                if scope.lower() == 'ads':
                    full_code = f"AD_{question_code}"
                else:
                    full_code = f"{scope.upper()}_{question_code}"
                category = self._categorize_question(question_code, scope)
                normalized_answer = self._normalize_answer(answer_value, full_code, scope)

                if category not in answers_by_category:
                    answers_by_category[category] = []

                answers_by_category[category].append({
                    'code': full_code,
                    'selected_answer': normalized_answer,
                    'notes': justification
                })

            assessments.append({
                'platform': platform_clean,
                'region_code': region_code,
                'scope': scope.upper(),
                'evaluation_date': eval_date,
                'analysts': str(analysts) if not pd.isna(analysts) else "",
                'answers_by_category': answers_by_category
            })

        return assessments

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
            yaml_data[key] = sorted(answers, key=lambda x: x['code'])

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

    def transform_all(self, platform_filter: str, ads_file: str = None, ugc_file: str = None):
        """Process all Excel files and generate YAML outputs."""
        print("Starting transformation...\n")

        if not ads_file or not ugc_file:
            raise ValueError("Both ads_file and ugc_file parameters must be provided")

        excel_files = {
            'ads': self.xlsx_dir / ads_file,
            'ugc': self.xlsx_dir / ugc_file
        }

        all_assessments = []
        platforms_processed = set()

        for scope, excel_path in excel_files.items():
            if not excel_path.exists():
                print(f"⚠ Warning: {excel_path} not found, skipping...")
                continue

            print(f"Processing {scope.upper()}: {excel_path.name}")
            assessments = self._process_excel_file(excel_path, scope)

            for assessment in assessments:
                if assessment['platform'] != platform_filter.lower():
                    continue

                yaml_data = self._generate_yaml_content(assessment)
                self._write_yaml_file(assessment['platform'], scope, yaml_data)
                all_assessments.append(assessment)
                platforms_processed.add(assessment['platform'])

            filtered_count = len([a for a in assessments if a['platform'] == platform_filter.lower()])
            print(f"  Processed {filtered_count} {scope.upper()} assessment(s) for {platform_filter}\n")

        print("\nGenerating QMD files from template...")
        qmd_created = []
        qmd_skipped = []

        for platform in sorted(platforms_processed):
            if self._create_qmd_from_template(platform):
                qmd_created.append(platform)
            else:
                qmd_skipped.append(platform)
                print(f"  Skipped {platform}: missing ads.yml or ugc.yml")

        print(f"\n✓ Created {len(qmd_created)} QMD files")
        if qmd_skipped:
            print(f"  Skipped {len(qmd_skipped)} platforms (incomplete data)")

        print("\nTransformation complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Transform Excel assessment responses to YAML format"
    )
    parser.add_argument(
        "--platform",
        required=True,
        help="Platform name to process (e.g., reddit, youtube, tiktok)"
    )
    parser.add_argument(
        "--scope-type",
        choices=["global", "regional"],
        default="global",
        help="Scope type: global or regional (default: global)"
    )
    parser.add_argument(
        "--region",
        help="Region code (required for regional scope, e.g., BR, EU, UK)"
    )
    parser.add_argument(
        "--ads-file",
        required=True,
        help="ADS Excel filename in xlsx_backups"
    )
    parser.add_argument(
        "--ugc-file",
        required=True,
        help="UGC Excel filename in xlsx_backups"
    )

    args = parser.parse_args()

    if args.scope_type == "regional" and not args.region:
        parser.error("--region is required when --scope-type is regional")

    base_dir = Path(__file__).parent.parent
    transformer = ExcelToYAMLTransformer(
        base_dir,
        scope_type=args.scope_type,
        region_code=args.region
    )
    transformer.transform_all(
        platform_filter=args.platform,
        ads_file=args.ads_file,
        ugc_file=args.ugc_file
    )


if __name__ == "__main__":
    main()
