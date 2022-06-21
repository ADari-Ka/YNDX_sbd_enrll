class OfferAndCategory:
    """Node class"""

    uid: str
    name: str
    date: str
    parentId: str
    type: str
    price: int
    children: list

    def __int__(self, uid: str, name: str, type: str, date: str):
        """Receive BASE fields for initializing node object"""

        self.uid = uid
        self.name = name
        self.type = type

        self.parentId = '-1'
        self.price = 0

        self.update_date(date)

        self.children = list()

        self.parent = None

    def update_date(self, date):
        """
        Update date by updating fields;
        Also update parent's date field

        :param date:
        :return:
        """
        self.date = date
        if not self.parent or self.parent.uid == "-1":
            return
        else:
            self.parent.update_date(date)

    def add_parent(self, parent_id: str):
        """Add parent field value"""
        self.parentId = parent_id

    def add_child(self, node):
        """Append new child in children list"""
        if node not in self.children:
            self.children.append(node)

    def remove_child(self, node):
        """Remove child from the children list"""
        self.children = self.children.pop(self.children.index(node))

    def add_price(self, price):
        """Add price field"""
        self.price = int(price)

    def get_price(self) -> (int, int):
        """
        Get parts of category's price (usually)

        :return: (total child offers sum, number of child offers)
        """
        if self.type == "OFFER":
            return self.price, 1
        else:
            if not self.children:
                return 0, 0
            else:
                summa, count = 0, 0
                for node in self.children:
                    temp = node.get_price()
                    summa += temp[0]
                    count += temp[1]
                return summa, count

    def __str__(self):
        return self.uid

    def __add__(self, other):
        """
        Updating fields with other's node data

        :param other: node object (OfferAndCategory class)
        :return:
        """
        self.name = other.name
        self.parentId = other.parentId
        self.type = other.type
        self.price = other.price

        self.parent = other.parent
        self.children = other.children

        self.update_date(other.date)

    def to_dict(self, need_children: bool = True) -> dict:
        """
        Cast node object to dictionary with needed fields

        :param need_children: flag is using for control sales/node gets requests
        :return: dictionary obj.
        """
        result = {}

        result["id"] = self.uid
        result["type"] = self.type
        result["name"] = self.name
        result["date"] = self.date
        p = self.get_price()
        result["price"] = int(p[0] / p[1]) if p[0] and p[1] else None

        # don't need to write base parent node's id
        result["parentId"] = self.parentId if self.parentId != "-1" else None

        if need_children:
            result["children"] = []

            if self.children:
                for node in self.children:
                    result["children"].append(node.to_dict())  # recursive getting children

            result["children"] = result["children"] if result["children"] else None

        return result
