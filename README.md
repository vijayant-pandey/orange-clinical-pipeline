![CI](https://github.com/vijayant-pandey/orange-clinical-pipeline/actions/workflows/ci.yml/badge.svg)
![Release](https://github.com/vijayant-pandey/orange-clinical-pipeline/actions/workflows/release.yml/badge.svg)


# Orange Clinical Trials Data Pipeline (Python + MySQL + SQL)

This project demonstrates a simple data pipeline for clinical-trial-like data:
- Generate 10,000 realistic trial records (CSV)
- Load into MySQL (XAMPP)
- Run analytics using SQL (filtering, trends, safety, success rates)
- CI validates dataset + runs tests via GitHub Actions

## Folder structure
- data/raw/ : generated CSV data
- src/generate/ : data generator
- src/load/ : MySQL loader
- sql/queries/ : interview SQL queries
- tests/ : automated checks
- .github/workflows/ : CI pipelines

## Phase 1: Generate CSV
```bash
python src/generate/generate_trials.py
