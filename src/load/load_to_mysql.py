import pandas as pd
import numpy as np
import mysql.connector


CSV_PATH = "data/raw/clinical_trials_10000.csv"

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""  # XAMPP default is often empty
MYSQL_DB = "orange_trials"
MYSQL_TABLE = "clinical_trials"


def nan_to_none(x):
    # Convert pandas/numpy NaN to Python None -> becomes SQL NULL
    if x is None:
        return None
    try:
        # works for float('nan') and np.nan
        if isinstance(x, float) and np.isnan(x):
            return None
    except Exception:
        pass
    return x


def main():
    # 1) Read CSV
    df = pd.read_csv(CSV_PATH)

    # 2) Ensure dates are in 'YYYY-MM-DD'
    df["enrollment_date"] = pd.to_datetime(df["enrollment_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["visit_date"] = pd.to_datetime(df["visit_date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # 3) Force numeric columns (important for MySQL insert)
    numeric_cols = [
        "trial_record_id", "age",
        "baseline_marker", "followup_marker",
        "systolic_bp", "diastolic_bp", "heart_rate",
        "success_flag"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4) Convert NaN -> None across the whole dataframe
    df = df.replace({np.nan: None})

    # 5) Prepare rows as tuples (and ensure followup_marker NULL works)
    rows = []
    for row in df.itertuples(index=False, name=None):
        row = tuple(nan_to_none(x) for x in row)
        rows.append(row)

    # 6) Connect to MySQL
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
    )
    cursor = conn.cursor()

    insert_sql = f"""
        INSERT INTO {MYSQL_TABLE} (
            trial_record_id, patient_id, age, sex, site_name, trial_phase, drug_code,
            therapeutic_area, study_arm, enrollment_date, visit_date, baseline_marker,
            followup_marker, systolic_bp, diastolic_bp, heart_rate, adverse_event,
            adverse_event_severity, outcome, success_flag
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s
        )
    """

    # 7) Batch insert
    batch_size = 1000
    total = len(rows)

    for start in range(0, total, batch_size):
        batch = rows[start:start + batch_size]
        cursor.executemany(insert_sql, batch)
        conn.commit()
        print(f"Inserted {min(start + batch_size, total)} / {total}")

    cursor.close()
    conn.close()
    print("✅ Done loading CSV into MySQL.")


if __name__ == "__main__":
    main()
