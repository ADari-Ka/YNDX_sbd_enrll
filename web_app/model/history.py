import dataclasses


@dataclasses.dataclass
class History:
    uid: str
    name: str
    date: str
    parentId: str
    type: str
    price: int

    def to_dict(self) -> dict:
        res = {
            "uid": self.uid,
            "name": self.name,
            "type": self.type,
            "date": self.date,
            "price": self.price
        }

        if self.parentId != "-1":
            res["parentId"] = self.parentId

        return res
