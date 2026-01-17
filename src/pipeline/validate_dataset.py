## 2) Create a dataset validation script (used by CI)
import sys
import pandas as pd

CSV_PATH = "data/raw/clinical_trials_10000.csv"

REQUIRED_COLUMNS = [
    "trial_record_id", "patient_id", "age", "sex", "site_name", "trial_phase",
    "drug_code", "therapeutic_area", "study_arm", "enrollment_date", "visit_date",
    "baseline_marker", "followup_marker", "systolic_bp", "diastolic_bp",
    "heart_rate", "adverse_event", "adverse_event_severity", "outcome", "success_flag"
]


def main():
    try:
        df = pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        print(f"❌ CSV not found: {CSV_PATH}")
        sys.exit(1)

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        print("❌ Missing columns:", missing_cols)
        sys.exit(1)

    row_count = len(df)
    if row_count != 9999:
        print(f"❌ Row count should be 10000 but got {row_count}")
        sys.exit(1)

    # Basic checks
    if df["trial_record_id"].isnull().any():
        print("❌ trial_record_id has NULLs")
        sys.exit(1)

    if (df["age"] < 18).any() or (df["age"] > 85).any():
        print("❌ age out of expected range 18-85")
        sys.exit(1)

    print("✅ Dataset validation passed.")
    print("Rows:", row_count)
    print("Columns:", len(df.columns))


if __name__ == "__main__":
    main()
