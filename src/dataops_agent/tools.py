"""Fri 13 Nov lab: a @tool decorator that turns a typed Python function into an agent tool. YOU write it.

Lesson: ~/dev/learning/2026-11-13-python-decorators-introspection/README.md, section 5.
Standard library only: inspect, typing (get_type_hints, get_origin, get_args), functools.

    @tool
    def query_table(table: str, limit: int = 10) -> str:
        '''Run a read-only query against a table and return the first rows.'''

Rules (each one has a test in tests/test_tools.py):
  - @tool returns the original function unchanged in behaviour (calling it directly still works),
    and registers it in REGISTRY under its function name.
  - schema(name) returns the tool definition the Claude API expects:
        {"name": ..., "description": <first line of the docstring>,
         "input_schema": {"type": "object", "properties": {...}, "required": [...]}}
  - Type mapping: str -> "string", int -> "integer", float -> "number", bool -> "boolean",
    list[str] -> {"type": "array", "items": {"type": "string"}},
    Literal["a", "b"] -> {"type": "string", "enum": ["a", "b"]}.
  - A parameter with a default is not required, and its default appears as "default" in its property.
  - A parameter with no type hint, or an unsupported one, raises TypeError AT DECORATION TIME
    (fail when the code loads, not when the model calls it: last Monday's binding-time law).
  - call(name, args) runs the tool with a dict of arguments from the model:
    unknown tool -> ToolError; a missing required argument or an unexpected one -> ToolError;
    a value of the wrong type (e.g. "10" for an int) -> ToolError. Never coerce silently.
"""
REGISTRY: dict = {}


class ToolError(Exception):
    pass


def tool(fn):
    raise NotImplementedError


def schema(name: str) -> dict:
    raise NotImplementedError


def call(name: str, args: dict):
    raise NotImplementedError
