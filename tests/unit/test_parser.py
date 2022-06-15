import pytest

from web_app.entrypoints.routers.units_parser import parse_tools


def test_common_parser_correct():
    request_data = {"type": "test", "number": 10, "list_try": [1, 2, 3]}

    fields = [("type", str), ("number", int), ("list_try", list)]
    rules = parse_tools.ParseFields(fields)

    parse_tools.parser_match(request_data, rules)


def test_common_listed_parser_correct():
    request_data = [{"type": "listed_test", "number": 10, "list_try": [1, 2, 3]},
                    {"type": "listed_test", "number": -1, "list_try": [0, 1, 2]}]

    fields = [("type", str), ("number", int), ("list_try", list)]
    rules = parse_tools.ParseFields(fields, listed=True)

    parse_tools.parser_match(request_data, rules)


def test_common_parser_with_getter_correct():
    request_data = {"items": {"type": "test_with_getter", "number": 10, "list_try": [1, 2, 3]}}

    fields = [("type", str), ("number", int), ("list_try", list)]
    rules = parse_tools.ParseFields(fields, data_getter="items")

    parse_tools.parser_match(request_data, rules)


def test_common_listed_parser_with_getter_correct():
    request_data = {"items": [{"type": "listed_test", "number": 10, "list_try": [1, 2, 3]},
                              {"type": "listed_test", "number": -1, "list_try": [0, 1, 2]}]}

    fields = [("type", str), ("number", int), ("list_try", list)]
    rules = parse_tools.ParseFields(fields, listed=True, data_getter="items")

    parse_tools.parser_match(request_data, rules)


def test_common_listed_parser_with_getter_wrong_field():
    request_data = {"items": [{"wrong_field": "listed_test", "number": 10, "list_try": [1, 2, 3]},
                              {"type": "listed_test", "number": -1, "list_try": [0, 1, 2]}]}

    fields = [("type", str), ("number", int), ("list_try", list)]
    rules = parse_tools.ParseFields(fields, listed=True, data_getter="items")
    try:
        parse_tools.parser_match(request_data, rules)
    except parse_tools.ParseException:
        assert True


def test_common_listed_parser_with_getter_wrong_type():
    request_data = {"items": [{"type": "listed_test", "number": 10, "list_try": [1, 2, 3]},
                              {"type": "listed_test", "number": -1, "list_try": "wrong"}]}

    fields = [("type", str), ("number", int), ("list_try", list)]
    rules = parse_tools.ParseFields(fields, listed=True, data_getter="items")

    try:
        parse_tools.parser_match(request_data, rules)
    except parse_tools.ParseException:
        assert True
