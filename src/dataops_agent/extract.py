"""Wed 4 Nov lab: turn unstructured text into a validated Pydantic object with one tool call.

How it works:
  1. Send the schema as a tool: {"name": "record", "description": ..., "input_schema": Schema.model_json_schema()}
  2. Force the model to call it: tool_choice={"type": "tool", "name": "record"}
  3. Find the tool_use block in the response and validate its .input with Schema.model_validate(...)
  4. If validation fails, send the error back as a tool_result with is_error=True and ask again (max_retries times)
  5. Still invalid, or no tool call at all: raise ExtractionError
"""
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)
TOOL = "record"


class ExtractionError(Exception):
    pass


def extract(client, text: str, schema: type[T], *, model: str, max_tokens: int = 1024,
            instructions: str = "Extract the information from the text.", max_retries: int = 1) -> T:
    raise NotImplementedError("TODO")
