"""Run the extractor against the real API once your tests pass.

    uv run python -m dataops_agent.try_extract
"""
from dotenv import load_dotenv

from dataops_agent.config import load_config
from dataops_agent.extract import extract
from dataops_agent.llm import make_client
from dataops_agent.schemas import Incident, JobPosting


def main():
    load_dotenv()
    cfg = load_config()
    client = make_client()
    from tests.fixtures.alerts import FRESHNESS, JD, VOLUME
    for text, schema in [(FRESHNESS, Incident), (VOLUME, Incident), (JD, JobPosting)]:
        print(f"\n--- {schema.__name__} ---")
        print(extract(client, text, schema, model=cfg.model).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
