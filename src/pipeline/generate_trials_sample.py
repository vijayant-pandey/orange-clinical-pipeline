# import os
# import pandas as pd
# from src.generate.generate_trials import generate_trials

# OUT_PATH = os.path.join("data", "processed", "clinical_trials_ci_sample.csv")

# def main():
#     os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
#     df = generate_trials(2000)  # small for CI
#     df.to_csv(OUT_PATH, index=False)
#     print(f"✅ Generated CI sample: {OUT_PATH} rows={len(df)}")

# if __name__ == "__main__":
#     main()



import os
import sys

# Add project root to Python path so "src" imports work in CI
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.generate.generate_trials import generate_trials  # now works

OUT_PATH = os.path.join("data", "processed", "clinical_trials_ci_sample.csv")


def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df = generate_trials(2000)  # small for CI
    df.to_csv(OUT_PATH, index=False)
    print(f"✅ Generated CI sample: {OUT_PATH} rows={len(df)}")


if __name__ == "__main__":
    main()