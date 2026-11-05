"""Wed 11 Nov lab: measure the incident extractor instead of hoping it works. YOU write these.

Lesson: ~/dev/learning/2026-11-11-ai-evaluation-first/README.md, section 5.

Data shapes used everywhere below:
    golden    list of {"id": str, "expected": {"table": str, "check": str, "severity": str}}
    predicted dict id -> {"table": ..., "check": ..., "severity": ...}   (a missing id = the model failed)

Rules (each one has a test in tests/test_evals.py):
    field_accuracy     share of golden examples whose predicted[field] equals expected[field].
                       A missing prediction counts as wrong. Table names compare case-insensitively.
    precision_recall   for one field and one "positive" value (e.g. severity == "critical"):
                       precision = TP / (TP + FP), recall = TP / (TP + FN). Return 0.0 when a denominator is 0.
    slice_report       exact-match accuracy (all three fields right) per value of expected[by],
                       e.g. {"freshness": 1.0, "schema": 0.5}.
    agreement          given several runs of the same golden set (a list of `predicted` dicts), the share
                       of examples where every run gave the same value for `field`. Measures non-determinism.
    gate               given a report dict of metric name -> value and thresholds name -> minimum,
                       return a sorted list of human-readable failures, e.g. ["severity_acc 0.70 < 0.80"].
                       An empty list means the release may ship.
"""

FIELDS = ("table", "check", "severity")


def field_accuracy(golden: list[dict], predicted: dict[str, dict], field: str) -> float:
    raise NotImplementedError


def precision_recall(golden: list[dict], predicted: dict[str, dict], field: str, positive: str) -> tuple[float, float]:
    raise NotImplementedError


def slice_report(golden: list[dict], predicted: dict[str, dict], by: str = "check") -> dict[str, float]:
    raise NotImplementedError


def agreement(golden: list[dict], runs: list[dict[str, dict]], field: str) -> float:
    raise NotImplementedError


def gate(report: dict[str, float], thresholds: dict[str, float]) -> list[str]:
    raise NotImplementedError
