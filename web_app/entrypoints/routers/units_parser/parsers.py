from .parse_tools import ParseFields

from model.offer_category import Type

importParser = ParseFields([('items', list), ('updateDate', str)])

importUnitParser = ParseFields([("id", str),
                                ("name", str),
                                ("type", Type)],
                               listed=True,
                               data_getter='items')
