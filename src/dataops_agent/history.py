"""Wed 4 Nov drill (by hand): keep a conversation inside a token budget."""
from collections.abc import Callable


def trim_history(messages: list[dict], budget: int, count: Callable[[dict], int]) -> list[dict]:
    """Keep the newest messages whose token counts fit in budget.

    - Drop from the oldest end.
    - Never drop the last message, even if it alone is over budget.
    - The result must start with a "user" message (the API requires it).
    """
    raise NotImplementedError("TODO")
