# Data Transparency Index (private repo)

A Quarto-based research reporting system for evaluating social media platform transparency across multiple regions, produced by [NetLab/UFRJ](https://netlab.eco.ufrj.br).

Assessments cover two frameworks: **User-Generated Content (UGC)** and **Advertising (ADS)** data transparency, scored using a weighted methodology (0–100).

## Public repo

The published report lives at [`NetLab-ECO-UFRJ/transparency_index`](https://github.com/NetLab-ECO-UFRJ/transparency_index), deployed via GitHub Pages. That repo is maintained as the `public` branch of this repo and contains only the Quarto landing page — no assessment data, scripts, or utilities.

To update the public repo:
```bash
git checkout public
# make changes
git push --force public public:main
git checkout main
```

## Setup

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv sync

# Install Quarto: https://quarto.org/docs/get-started/
```

## Rendering

```bash
uv run quarto render        # full book → _output/
uv run quarto preview       # live reload
```

## Importing data from Excel

```bash
# Remove existing platform data before reimporting
rm -rf data/global/<platform>

# Global scope
uv run python scripts/transform_excel_to_yaml.py \
  --platform bluesky \
  --scope-type global \
  --ads-file "Advertising Framework (respostas).xlsx" \
  --ugc-file "UGC Framework (respostas).xlsx"

# Regional scope
uv run python scripts/transform_excel_to_yaml.py \
  --platform x \
  --scope-type regional \
  --region BR \
  --ads-file "Advertising Framework (respostas).xlsx" \
  --ugc-file "UGC Framework (respostas).xlsx"
```

Excel files go in `data/backups/xlsx/`. After import, add the new platform to `_quarto.yml`.

## Project structure

```
data/
├── questions_ugc_2025.yml / questions_ads_2025.yml   # framework definitions
├── global/<platform>/ugc.yml, ads.yml                # global assessments
└── regional/<REGION>/<platform>/ugc.yml, ads.yml     # regional assessments

utils/         # scoring, loading, and rendering helpers
scripts/       # Excel → YAML import scripts
chapters/      # report chapters and platform appendices
```
