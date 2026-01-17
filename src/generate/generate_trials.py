import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker("en_IN")
random.seed(42)
np.random.seed(42)

OUTPUT_PATH = os.path.join("data", "raw", "clinical_trials_10000.csv")


def pick_weighted(options, weights):
    return random.choices(options, weights=weights, k=1)[0]


def generate_trials(n=10000):
    """
    Generates realistic-ish clinical trial rows:
    - patient demographics
    - trial phase, site, drug
    - lab markers and outcomes
    - adverse events + severity
    - enrollment/visit dates
    """

    phases = ["Phase I", "Phase II", "Phase III", "Phase IV"]
    phase_weights = [0.15, 0.25, 0.45, 0.15]

    sites = [
        "Indore Medical Institute",
        "Bhopal Research Hospital",
        "AIIMS Delhi",
        "Apollo Chennai",
        "Fortis Mumbai",
        "PGI Chandigarh",
        "NIMHANS Bengaluru",
        "Kolkata Clinical Center",
    ]

    drugs = [
        ("ORX-101", "Oncology"),
        ("ORX-202", "Diabetes"),
        ("ORX-303", "Cardiology"),
        ("ORX-404", "Neurology"),
        ("ORX-505", "Infectious Disease"),
        ("ORX-606", "Rheumatology"),
    ]

    arms = ["Placebo", "Low Dose", "High Dose"]
    arm_weights = [0.30, 0.35, 0.35]

    sex_options = ["M", "F"]
    outcomes = ["Improved", "No Change", "Worsened"]
    outcome_weights = [0.55, 0.30, 0.15]

    adverse_events = ["None", "Nausea", "Headache", "Rash", "Fatigue", "Dizziness", "Fever"]
    ae_weights = [0.55, 0.12, 0.12, 0.06, 0.07, 0.04, 0.04]

    severity_levels = ["None", "Mild", "Moderate", "Severe"]
    severity_weights = [0.55, 0.25, 0.15, 0.05]

    base_date = datetime(2023, 1, 1)

    rows = []
    for i in range(1, n + 1):
        patient_id = f"PT-{i:05d}"

        age = int(np.clip(np.random.normal(loc=45, scale=16), 18, 85))
        sex = random.choice(sex_options)

        phase = pick_weighted(phases, phase_weights)
        site = random.choice(sites)

        drug_code, therapeutic_area = random.choice(drugs)
        arm = pick_weighted(arms, arm_weights)

        # Enrollment and visit dates
        enrollment_offset = random.randint(0, 700)  # within ~2 years
        enrollment_date = base_date + timedelta(days=enrollment_offset)

        visit_days = random.choice([7, 14, 28, 56, 90])
        visit_date = enrollment_date + timedelta(days=visit_days)

        # Baseline & follow-up biomarkers (simplified)
        # Example: HbA1c for diabetes-ish or CRP for inflammation-ish etc
        baseline_marker = float(np.clip(np.random.normal(loc=7.2, scale=1.2), 3.5, 14.0))
        followup_marker = baseline_marker + float(np.random.normal(loc=-0.4, scale=0.9))

        # Blood pressure & heart rate
        systolic = int(np.clip(np.random.normal(128, 18), 90, 190))
        diastolic = int(np.clip(np.random.normal(82, 12), 50, 120))
        heart_rate = int(np.clip(np.random.normal(78, 14), 45, 130))

        # Outcome and adverse events
        outcome = pick_weighted(outcomes, outcome_weights)
        adverse_event = pick_weighted(adverse_events, ae_weights)

        # Make severity consistent with AE
        if adverse_event == "None":
            severity = "None"
        else:
            severity = pick_weighted(severity_levels, severity_weights)

        # A crude "trial success flag" (for analytics)
        success_flag = 1 if (outcome == "Improved" and followup_marker < baseline_marker) else 0

        rows.append(
            {
                "trial_record_id": i,
                "patient_id": patient_id,
                "age": age,
                "sex": sex,
                "site_name": site,
                "trial_phase": phase,
                "drug_code": drug_code,
                "therapeutic_area": therapeutic_area,
                "study_arm": arm,
                "enrollment_date": enrollment_date.date().isoformat(),
                "visit_date": visit_date.date().isoformat(),
                "baseline_marker": round(baseline_marker, 2),
                "followup_marker": round(followup_marker, 2),
                "systolic_bp": systolic,
                "diastolic_bp": diastolic,
                "heart_rate": heart_rate,
                "adverse_event": adverse_event,
                "adverse_event_severity": severity,
                "outcome": outcome,
                "success_flag": success_flag,
            }
        )

    df = pd.DataFrame(rows)

    # Introduce a tiny bit of "mess" for real-life cleaning practice
    # 1% missing followup_marker
    mask = np.random.rand(len(df)) < 0.01
    df.loc[mask, "followup_marker"] = np.nan

    return df


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df = generate_trials(10000)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Generated: {OUTPUT_PATH}")
    print(df.head(5).to_string(index=False))
    print("\nRows:", len(df))


if __name__ == "__main__":
    main()
