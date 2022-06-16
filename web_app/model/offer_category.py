import uuid
from datetime import datetime

from dataclasses import dataclass
from enum import Enum


class OfferAndCategory:
    uid: str
    name: str
    _date: datetime
    parentId: str
    type: str
    price: int
    children: list

    def __int__(self, uid: str, name: str, e_type: str, date: str):
        self.uid = uid
        self.name = name
        self.type = e_type

        self.children = []

        self.parentId = ''
        self.price = -1

        self._date = datetime.fromisoformat(date)

    def add_parent(self, parent_id: str):
        self.parentId = parent_id

    def add_child(self, node):
        if not self.children:
            self.children = [node]
        else:
            self.children.append(node)

    def add_price(self, price):
        self.price = int(price)

    def get_price(self):
        if self.type == "OFFER":
            return self.price
        else:
            if not self.children:
                return None
            else:
                count, summ = 0, 0
                for node in self.children:
                    price = node.get_price()
                    summ += price if price else 0
                    count += 1 if price else 0

                return int(summ / count)

    @property
    def date(self):
        return str(self._date.isoformat())

    @date.setter
    def date(self, new):
        self._date = datetime.fromisoformat(new)

    def __add__(self, other):
        self.name = other.name
        self.date = other.date
        self.parentId = other.parentId
        self.type = other.type
        self.price = other.price
        self.children = other.children

    def to_dict(self) -> dict:
        result = {}

        result["id"] = self.uid
        result["type"] = self.type
        result["name"] = self.name
        result["date"] = self.date

        result["parentId"] = self.parentId if self.parentId else None

        price = self.get_price()
        result["price"] = None if not price else price

        result["children"] = []

        if self.children:
            for node in self.children:
                result["children"].append(node.to_dict())

        return result
