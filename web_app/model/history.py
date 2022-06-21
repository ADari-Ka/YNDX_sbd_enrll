import dataclasses


@dataclasses.dataclass
class History:
    """Class for storing history records of nodes updates"""

    uid: str
    name: str
    date: str
    parentId: str
    type: str
    price: int

    def to_dict(self) -> dict:
        res = {"id": self.uid, "name": self.name, "type": self.type, "date": self.date,
               "price": self.price if self.price else None}

        if self.parentId != "-1":
            res["parentId"] = self.parentId

        return res
