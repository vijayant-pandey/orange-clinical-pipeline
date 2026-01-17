import os
import pandas as pd

CSV_PATH = "data/raw/clinical_trials_10000.csv"
OUT_DIR = "reports"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df = pd.read_csv(CSV_PATH)

    # Report 1: Drug success leaderboard (like Q5)
    drug_success = (
        df.groupby("drug_code")
        .agg(total=("success_flag", "size"), successes=("success_flag", "sum"))
        .reset_index()
    )
    drug_success["success_rate_pct"] = (100 * drug_success["successes"] / drug_success["total"]).round(2)
    drug_success = drug_success.sort_values(["success_rate_pct", "total"], ascending=[False, False])

    drug_success.to_csv(os.path.join(OUT_DIR, "drug_success_leaderboard.csv"), index=False)

    # Report 2: Severe events by drug (like Q9)
    severe = df[df["adverse_event_severity"] == "Severe"]
    severe_by_drug = (
        severe.groupby("drug_code")
        .size()
        .reset_index(name="severe_events")
        .sort_values("severe_events", ascending=False)
    )
    severe_by_drug.to_csv(os.path.join(OUT_DIR, "severe_events_by_drug.csv"), index=False)

    # Report 3: Monthly enrollment trend (like Q12)
    df["enrollment_date"] = pd.to_datetime(df["enrollment_date"], errors="coerce")
    df["month"] = df["enrollment_date"].dt.strftime("%Y-%m")
    monthly = (
        df.groupby("month")
        .size()
        .reset_index(name="enrollments")
        .sort_values("month")
    )
    monthly.to_csv(os.path.join(OUT_DIR, "monthly_enrollment_trend.csv"), index=False)

    # Simple HTML summary (looks good in interviews)
    html_path = os.path.join(OUT_DIR, "summary.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write("<html><head><meta charset='utf-8'><title>Clinical Pipeline Report</title></head><body>")
        f.write("<h1>Clinical Trials Pipeline - Summary</h1>")
        f.write("<p>This report was generated automatically from the raw CSV dataset.</p>")

        f.write("<h2>Drug Success Leaderboard (Top 10)</h2>")
        f.write(drug_success.head(10).to_html(index=False))

        f.write("<h2>Severe Events by Drug</h2>")
        f.write(severe_by_drug.to_html(index=False))

        f.write("<h2>Monthly Enrollment Trend</h2>")
        f.write(monthly.to_html(index=False))

        f.write("</body></html>")

    print("✅ Reports generated in /reports")
    print("- drug_success_leaderboard.csv")
    print("- severe_events_by_drug.csv")
    print("- monthly_enrollment_trend.csv")
    print("- summary.html")


if __name__ == "__main__":
    main()
