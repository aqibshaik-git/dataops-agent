import pytest

from dataops_agent.evals import agreement, field_accuracy, gate, precision_recall, slice_report

GOLDEN = [
    {"id": "a", "expected": {"table": "marts.daily_spend", "check": "freshness", "severity": "critical"}},
    {"id": "b", "expected": {"table": "raw.ledger_events", "check": "volume", "severity": "high"}},
    {"id": "c", "expected": {"table": "staging.postings", "check": "null_rate", "severity": "medium"}},
    {"id": "d", "expected": {"table": "finance.postings", "check": "freshness", "severity": "critical"}},
]
PRED = {
    "a": {"table": "MARTS.DAILY_SPEND", "check": "freshness", "severity": "critical"},
    "b": {"table": "raw.ledger_events", "check": "volume", "severity": "critical"},
    "c": {"table": "staging.postings", "check": "schema", "severity": "medium"},
    # "d" missing: the model failed on it
}


def test_field_accuracy_counts_missing_as_wrong_and_ignores_table_case():
    assert field_accuracy(GOLDEN, PRED, "table") == pytest.approx(0.75)
    assert field_accuracy(GOLDEN, PRED, "severity") == pytest.approx(0.5)


def test_precision_recall_for_critical():
    p, r = precision_recall(GOLDEN, PRED, "severity", "critical")
    assert p == pytest.approx(0.5)   # predicted critical: a (right), b (wrong)
    assert r == pytest.approx(0.5)   # actual critical: a (found), d (missed)


def test_precision_recall_zero_denominators():
    assert precision_recall(GOLDEN, PRED, "severity", "low") == (0.0, 0.0)


def test_slice_report_by_check():
    assert slice_report(GOLDEN, PRED, by="check") == {"freshness": 0.5, "volume": 0.0, "null_rate": 0.0}


def test_agreement_across_runs():
    run2 = {**PRED, "b": {"table": "raw.ledger_events", "check": "volume", "severity": "high"}}
    run3 = dict(PRED)
    # severity: a agrees (critical x3), b disagrees, c agrees, d missing in all runs = agrees (all None)
    assert agreement(GOLDEN, [PRED, run2, run3], "severity") == pytest.approx(0.75)


def test_gate_lists_failures_only():
    report = {"table_acc": 0.95, "severity_acc": 0.70, "critical_recall": 1.0}
    assert gate(report, {"table_acc": 0.9, "severity_acc": 0.8, "critical_recall": 0.95}) == ["severity_acc 0.70 < 0.80"]
    assert gate(report, {"table_acc": 0.9}) == []
