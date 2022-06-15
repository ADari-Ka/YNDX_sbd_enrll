from model import OfferAndCategory


def node_create(data: dict, date: str) -> OfferAndCategory:
    node = OfferAndCategory(
        uid=data['id'],
        name=data['name'],
        type=data['type'],
        date=date
    )

    if 'parentId' in data.keys():
        node.add_parent(data['parentId'])
    if 'price' in data.keys():
        node.add_price(data['price'])
    elif node.type == False:
        raise TypeError
