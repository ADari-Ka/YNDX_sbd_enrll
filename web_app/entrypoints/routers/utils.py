from model import OfferAndCategory


def node_create(data: dict, date: str) -> OfferAndCategory:
    if data['type'] not in ["CATEGORY", "OFFER"]:
        raise TypeError

    date = date.replace("Z", "+00:00")

    node = OfferAndCategory(
        uid=data['id'],
        name=data['name'],
        type=data['type'],
        date=date
    )

    if 'parentId' in data.keys():
        node.add_parent(data['parentId'] if data['parentId'] else '')
    if 'price' in data.keys():
        if data['price'] <= 0:
            raise ValueError
        node.add_price(data['price'])

    if node.type == "CATEGORY" and "price" in data.keys():
        raise AttributeError

    if node.type == "OFFER" and "price" not in data.keys():
        raise AttributeError

    return node
