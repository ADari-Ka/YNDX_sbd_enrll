from typing import Dict, List, Tuple


class ParseException(BaseException):
    field: str
    types: Tuple[str, str]

    def __init__(self, field='', types=()):
        self.field = field
        self.types = types

    def __str__(self):
        if self.types:
            return f'Instead type "{self.types[0]}" got "{self.types[1]}" in field {self.field}'
        if self.field:
            return f'There is no field "{self.field}"'

        return 'Wrong format'


class ParseFields:
    rules: Dict[str, type]
    is_listed: bool

    data_getter: str

    def __init__(self, rules: List[Tuple[str, type]], listed=False, data_getter=''):
        self.rules = {}
        for rule in rules:
            self.rules[rule[0]] = rule[1]

        self.is_listed = listed
        self.data_getter = data_getter


def parser_match(
        request_body,
        parse_fields: ParseFields
):
    data = (request_body[parse_fields.data_getter]
            if parse_fields.data_getter else request_body) \
        if parse_fields.is_listed else ([request_body[parse_fields.data_getter]]
                                        if parse_fields.data_getter else [request_body])

    for element in data:
        for field in parse_fields.rules.keys():
            if field not in element.keys():
                raise ParseException(field=field)
            if type(element[field]) != parse_fields.rules[field]:
                raise ParseException(field=field, types=(parse_fields.rules[field], element[field]))
