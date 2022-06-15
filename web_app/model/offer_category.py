import uuid
from datetime import datetime

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Type(Enum):
    OFFER = False
    CATEGORY = True


class OfferAndCategory:
    uid: str
    name: str
    _date: datetime
    parentId: str
    type: Type
    price: int
    children: list

    def __int__(self, uid: str, name: str, e_type: Type, date: str):
        self.uid = uid
        self.name = name
        self.type = e_type
        self.children = [] if e_type else None

        self.parentId = ''
        self.price = -1

        self._date = datetime.fromisoformat(date)

    def add_parent(self, parent_id: str):
        self.parentId = parent_id

    def add_price(self, price):
        self.price = int(price)

    @property
    def date(self):
        return str(self._date.isoformat())

    @date.setter
    def date(self, new):
        self._date = datetime.fromisoformat(new)
