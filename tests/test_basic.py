import pandas as pd

CSV_PATH = "data/raw/clinical_trials_10000.csv"


def test_csv_exists_and_has_rows():
    df = pd.read_csv(CSV_PATH)
    assert len(df) == 10000


def test_required_columns_exist():
    df = pd.read_csv(CSV_PATH)
    required = {
        "trial_record_id", "patient_id", "age", "sex", "site_name", "trial_phase",
        "drug_code", "therapeutic_area", "study_arm", "enrollment_date", "visit_date",
        "baseline_marker", "followup_marker", "systolic_bp", "diastolic_bp",
        "heart_rate", "adverse_event", "adverse_event_severity", "outcome", "success_flag"
    }
    assert required.issubset(set(df.columns))
