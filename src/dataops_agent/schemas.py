"""Wed 4 Nov lab: the shapes the agent extracts. You write both models (Pydantic v2).

Incident: a data-quality incident on the payments platform, built from a raw alert.
    table            str   fully qualified table or topic, e.g. "marts.daily_spend"
    check            one of: freshness, volume, schema, null_rate, reconciliation, other
    severity         one of: low, medium, high, critical
    suspected_cause  str   one sentence; "unknown" if the alert gives no clue
    evidence         list[str], default empty: facts quoted from the alert

JobPosting: a job description, for the job-search persona.
    title, company, location        str
    work_mode                       one of: remote, hybrid, onsite, unknown
    office_days_per_week            int 0–5, or None
    salary_min_gbp, salary_max_gbp  int or None
    must_have_skills                list[str]
    nice_to_have_skills             list[str], default empty
    security_clearance_required     bool, default False

Use Literal for the fixed choices and Field(description=...) on anything the model might misread:
the descriptions go into the JSON schema the model sees, so they are part of the prompt.
"""
from pydantic import BaseModel


class Incident(BaseModel):
    pass  # TODO


class JobPosting(BaseModel):
    pass  # TODO
