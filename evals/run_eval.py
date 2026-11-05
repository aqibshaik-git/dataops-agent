"""Run the golden set through the real extractor and print a report. Needs your API key in .env.

    uv run python evals/run_eval.py --trials 3

YOU finish this after evals.py is green (lab if time, Wed 11 Nov). Shape:
    1. load evals/golden.jsonl
    2. for each trial, for each example: extract_incident(alert) -> {table, check, severity}; failures = missing
    3. report = {"table_acc", "check_acc", "severity_acc", "critical_precision", "critical_recall",
                 "severity_agreement"} plus slice_report by check
    4. print it as a table; exit 1 if gate(report, THRESHOLDS) is not empty (that's your CI regression gate)
"""
THRESHOLDS = {"table_acc": 0.9, "check_acc": 0.85, "severity_acc": 0.8, "critical_recall": 0.95}

if __name__ == "__main__":
    raise SystemExit("TODO: you write this (see the docstring)")
