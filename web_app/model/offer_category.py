import uuid
import datetime

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Type(Enum):
    OFFER = False
    Category = True


class OfferAndCategory:
    uid: str
    name: str
    date: datetime.datetime
    parentId: str
    type: Type
    price: int
    children: list

    def __int__(self, uid: str, name: str, e_type: Type):
        self.uid = uid
        self.name = name
        self.type = e_type

        self.date = datetime.datetime.now()

    def add_parent(self, parent_id: str):
        self.parentId = parent_id

    def add_price(self, price):
        self.price = int(price)
