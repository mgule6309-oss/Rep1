"""Run the Community Library Management System checks."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHECKS = [
    ("Database build and validation", "build_database.py"),
    ("Query optimisation analysis", "run_query_analysis.py"),
    ("Transaction tests", "test_transactions.py"),
]


def main():
    for description, script_name in CHECKS:
        script_path = Path(__file__).resolve().parent / script_name

        print(f"\n{'=' * 60}")
        print(f"Running: {description}")
        print(f"{'=' * 60}")

        if not script_path.exists():
            print(f"ERROR: Cannot find {script_name}")
            return 1

        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=PROJECT_ROOT,
            check=False,
        )

        if result.returncode != 0:
            print(f"\nFAILED: {description}")
            print("The remaining checks were not run.")
            return result.returncode

        print(f"\nPASSED: {description}")

    print("\nAll checks completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
