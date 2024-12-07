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


def query_params(url: str) -> Dict[str, str]:
    """Extract the query parameters from a url"""
    res: dict = {}
    split = url.split("?")
    if len(split) < 2:
        return res
    params = split[1]
    params = params.split("&")
    for value in params:
        kv = value.split("=")
        res[kv[0]] = str(kv[1])

    return res


Grouping = Tuple[Dict[str, Any], List[Dict]]


def group_list_data(
    data: List[Dict[str, Any]],
    grouping_key: str,
    *label_keys,
) -> List[Dict[str, Any]]:
    """grouping_key must be a valid key in all the dictionaries inside the data list.
    The value of grouping key must be an integer and the value of label key must be a string
    """
    result: Dict[int, Grouping] = {}
    for value in data:
        grouping_value = value[grouping_key]
        group = result.get(grouping_value)
        if group is None:
            group = ({key: value[key] for key in label_keys}, [])
            result[grouping_value] = group
        group[1].append(value)

    return [{**i[0], "data": i[1]} for i in result.values()]


def swap_keys(data: Dict[str, Any], key_swaps: Dict[str, str]):
    for key, swap in key_swaps.items():
        data[swap] = data.pop(key)
    return data
