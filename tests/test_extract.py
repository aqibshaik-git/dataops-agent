from types import SimpleNamespace

import pytest

from dataops_agent.extract import ExtractionError, extract
from dataops_agent.schemas import Incident, JobPosting
from tests.fixtures.alerts import FRESHNESS, JD


def tool_message(payload, block_id="tu_1"):
    return SimpleNamespace(content=[SimpleNamespace(type="tool_use", id=block_id, name="record", input=payload)],
                           stop_reason="tool_use", usage=SimpleNamespace(input_tokens=300, output_tokens=80))


class ScriptedClient:
    """Returns the scripted responses in order and records every request."""

    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []
        outer = self

        class Messages:
            def create(self, **kwargs):
                outer.requests.append(kwargs)
                return outer.responses.pop(0)

        self.messages = Messages()


GOOD_INCIDENT = {"table": "marts.daily_spend", "check": "freshness", "severity": "critical",
                 "suspected_cause": "Upstream staging.postings failed after a Kafka Connect connection reset.",
                 "evidence": ["4h 40m late", "connection reset by peer from kafka-connect"]}


def test_returns_a_validated_model():
    client = ScriptedClient(tool_message(GOOD_INCIDENT))
    incident = extract(client, FRESHNESS, Incident, model="m")
    assert isinstance(incident, Incident)
    assert incident.check == "freshness" and incident.severity == "critical"


def test_forces_the_tool_and_sends_the_schema():
    client = ScriptedClient(tool_message(GOOD_INCIDENT))
    extract(client, FRESHNESS, Incident, model="m")
    req = client.requests[0]
    assert req["tool_choice"] == {"type": "tool", "name": "record"}
    assert req["tools"][0]["input_schema"] == Incident.model_json_schema()
    assert FRESHNESS.strip() in req["messages"][0]["content"]


def test_retries_once_with_the_validation_error():
    bad = dict(GOOD_INCIDENT, severity="apocalyptic")
    client = ScriptedClient(tool_message(bad, "tu_bad"), tool_message(GOOD_INCIDENT, "tu_ok"))
    incident = extract(client, FRESHNESS, Incident, model="m")
    assert incident.severity == "critical"
    retry = client.requests[1]["messages"]
    assert retry[-1]["content"][0]["type"] == "tool_result"
    assert retry[-1]["content"][0]["tool_use_id"] == "tu_bad"
    assert retry[-1]["content"][0]["is_error"] is True


def test_gives_up_after_max_retries():
    bad = dict(GOOD_INCIDENT, check="vibes")
    client = ScriptedClient(tool_message(bad), tool_message(bad))
    with pytest.raises(ExtractionError):
        extract(client, FRESHNESS, Incident, model="m", max_retries=1)


def test_same_function_parses_a_job_description():
    payload = {"title": "Senior Java Engineer", "company": "Unknown (agency)", "work_mode": "hybrid",
               "office_days_per_week": 2, "location": "London", "salary_min_gbp": 95000, "salary_max_gbp": 110000,
               "must_have_skills": ["Java 17+", "Spring Boot", "Kafka", "PostgreSQL"],
               "nice_to_have_skills": ["Kubernetes", "Terraform"], "security_clearance_required": False}
    job = extract(ScriptedClient(tool_message(payload)), JD, JobPosting, model="m")
    assert job.work_mode == "hybrid" and job.office_days_per_week == 2
    assert "Kafka" in job.must_have_skills


def test_office_days_must_be_0_to_5():
    with pytest.raises(Exception):
        JobPosting(title="x", company="y", work_mode="hybrid", office_days_per_week=7, location="London",
                   must_have_skills=[])
