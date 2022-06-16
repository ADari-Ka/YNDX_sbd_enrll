from typing import Union

from .parse_tools import ParseFields

importParser = ParseFields([('items', list), ('updateDate', str)])

importUnitParser = ParseFields([("id", str),
                                ("name", str),
                                ("type", str)],
                               listed=True,
                               data_getter='items')
