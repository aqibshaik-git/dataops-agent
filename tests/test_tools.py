from typing import Literal

import pytest

from dataops_agent import tools
from dataops_agent.tools import REGISTRY, ToolError, call, schema, tool


def setup_function():
    REGISTRY.clear()


def test_decorated_function_still_works_and_is_registered():
    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
    assert add(2, 3) == 5
    assert "add" in REGISTRY


def test_schema_types_defaults_and_required():
    @tool
    def query_table(table: str, limit: int = 10, sample: float = 0.5, dry_run: bool = False) -> str:
        """Run a read-only query.

        More detail that should not appear in the description.
        """
    s = schema("query_table")
    assert s["name"] == "query_table"
    assert s["description"] == "Run a read-only query."
    props = s["input_schema"]["properties"]
    assert props["table"] == {"type": "string"}
    assert props["limit"] == {"type": "integer", "default": 10}
    assert props["sample"] == {"type": "number", "default": 0.5}
    assert props["dry_run"] == {"type": "boolean", "default": False}
    assert s["input_schema"]["required"] == ["table"]
    assert s["input_schema"]["type"] == "object"


def test_list_and_literal():
    @tool
    def tag(names: list[str], severity: Literal["low", "high"]) -> None:
        """Tag things."""
    props = schema("tag")["input_schema"]["properties"]
    assert props["names"] == {"type": "array", "items": {"type": "string"}}
    assert props["severity"] == {"type": "string", "enum": ["low", "high"]}


def test_bad_hints_fail_at_decoration_time():
    with pytest.raises(TypeError):
        @tool
        def untyped(x):
            """No hint."""
    with pytest.raises(TypeError):
        @tool
        def weird(x: dict) -> None:
            """Unsupported type."""


def test_call_validates_strictly():
    @tool
    def read_logs(job: str, lines: int = 50) -> str:
        """Read logs."""
        return f"{job}:{lines}"
    assert call("read_logs", {"job": "dbt"}) == "dbt:50"
    assert call("read_logs", {"job": "dbt", "lines": 5}) == "dbt:5"
    for bad in ({}, {"job": "dbt", "extra": 1}, {"job": "dbt", "lines": "10"}, {"job": 3}):
        with pytest.raises(ToolError):
            call("read_logs", bad)
    with pytest.raises(ToolError):
        call("nope", {})


def test_bool_is_not_an_int():
    @tool
    def n(count: int) -> int:
        """Count."""
        return count
    with pytest.raises(ToolError):
        call("n", {"count": True})
