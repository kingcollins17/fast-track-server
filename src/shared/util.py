from typing import Dict, Tuple, List, Any, Union


def example_response(
    status: int, example: Union[Dict, List[Dict]], description: str | None = None
) -> Dict:
    return {
        status: {
            "description": description or "Successful response",
            "content": {"application/json": {"example": example}},
        },
    }
