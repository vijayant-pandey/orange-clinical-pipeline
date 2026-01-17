import pandas as pd
import numpy as np
import mysql.connector

CSV_PATH = "data/processed/clinical_trials_ci_sample.csv"

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "orange_trials"
MYSQL_TABLE = "clinical_trials"

def main():
    df = pd.read_csv(CSV_PATH)

    df["enrollment_date"] = pd.to_datetime(df["enrollment_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    numeric_cols = [
        "trial_record_id", "age",
        "baseline_marker", "followup_marker",
        "systolic_bp", "diastolic_bp", "heart_rate",
        "success_flag"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.replace({np.nan: None})

    rows = [tuple(x if x == x else None for x in r) for r in df.itertuples(index=False, name=None)]

    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
    )
    cur = conn.cursor()

    insert_sql = f"""
        INSERT INTO {MYSQL_TABLE} (
            trial_record_id, patient_id, age, sex, site_name, trial_phase, drug_code,
            therapeutic_area, study_arm, enrollment_date, visit_date, baseline_marker,
            followup_marker, systolic_bp, diastolic_bp, heart_rate, adverse_event,
            adverse_event_severity, outcome, success_flag
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cur.executemany(insert_sql, rows)
    conn.commit()

    cur.close()
    conn.close()
    print(f"✅ Loaded {len(rows)} rows into MySQL (CI).")

if __name__ == "__main__":
    main()
