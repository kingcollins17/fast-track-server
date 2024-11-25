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


def page_offset(page: int, per_page: int):
    if page < 0:
        return 0
    return (page - 1) * per_page


def role_has_permission(roles: List[Dict], permission: str) -> bool:
    """Search for a specific permission in a member's organization roles"""
    has_permission = False
    for role in roles:
        if role[permission] == True:
            has_permission = True
            break
    return has_permission
