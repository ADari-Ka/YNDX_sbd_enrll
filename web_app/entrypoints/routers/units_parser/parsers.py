from .parse_tools import ParseFields

importParser = ParseFields([('items', list), ('updateDate', str)])  # from OpenAPI specification

# from OpenAPI specification
importUnitParser = ParseFields([("id", str),
                                ("name", str),
                                ("type", str)],
                               listed=True,
                               data_getter='items')
