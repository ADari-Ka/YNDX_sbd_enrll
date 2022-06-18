from datetime import datetime


class OfferAndCategory:
    uid: str
    name: str
    date: str
    parentId: str
    type: str
    price: int
    children: list

    def __int__(self, uid: str, name: str, type: str, date: str):
        self.uid = uid
        self.name = name
        self.type = type

        self.parentId = '-1'
        self.price = 0

        self.date = date

        self.children = list()

    def add_parent(self, parent_id: str):
        self.parentId = parent_id

    def add_child(self, node):
        if node not in self.children:
            self.children.append(node)

    def remove_child(self, node):
        self.children = self.children.pop(self.children.index(node))

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

    def __str__(self):
        return self.uid

    def __add__(self, other):
        self.name = other.name
        self.date = other.date
        self.parentId = other.parentId
        self.type = other.type
        self.price = other.price
        # self.children = other.children

    def to_dict(self) -> dict:
        result = {}

        result["id"] = self.uid
        result["type"] = self.type
        result["name"] = self.name
        result["date"] = self.date
        result["price"] = self.get_price()

        result["parentId"] = self.parentId if self.parentId != "-1" else None

        result["children"] = []

        if self.children:
            for node in self.children:
                result["children"].append(node.to_dict())

        result["children"] = result["children"] if result["children"] else None

        return result
