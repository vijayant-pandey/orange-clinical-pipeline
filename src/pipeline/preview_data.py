import pandas as pd

path = "data/raw/clinical_trials_10000.csv"
df = pd.read_csv(path)

print("Total rows:", len(df))

# Example: filter Phase III + High Dose + Severe adverse events
filtered = df[
    (df["trial_phase"] == "Phase III")
    & (df["study_arm"] == "High Dose")
    & (df["adverse_event_severity"] == "Severe")
]

print("\nFiltered (Phase III + High Dose + Severe):", len(filtered))
print(filtered.head(10).to_string(index=False))

# Sort by baseline_marker descending (top high-risk)
sorted_df = df.sort_values("baseline_marker", ascending=False)
print("\nTop 5 baseline_marker:")
print(sorted_df[["patient_id", "trial_phase", "drug_code", "baseline_marker"]].head(5).to_string(index=False))
