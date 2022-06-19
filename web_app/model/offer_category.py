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

        self.parent = None

    def update_date(self, date):
        self.date = date
        if not self.parent or self.parent.uid == "-1":
            return
        else:
            self.parent.update_date(date)

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
            return self.price, 1
        else:
            if not self.children:
                return 0, 0
            else:
                summ = 0
                count = 0
                for node in self.children:
                    temp = node.get_price()
                    summ += temp[0]
                    count += temp[1]
                return summ, count

    def __str__(self):
        return self.uid

    def __add__(self, other):
        self.name = other.name
        self.parentId = other.parentId
        self.type = other.type
        self.price = other.price

        self.parent = other.parent
        self.children = other.children

        self.update_date(other.date)

    def to_dict(self) -> dict:
        result = {}

        result["id"] = self.uid
        result["type"] = self.type
        result["name"] = self.name
        result["date"] = self.date
        p = self.get_price()
        result["price"] = int(p[0] / p[1])

        result["parentId"] = self.parentId if self.parentId != "-1" else None

        result["children"] = []

        if self.children:
            for node in self.children:
                result["children"].append(node.to_dict())

        result["children"] = result["children"] if result["children"] else None

        return result
