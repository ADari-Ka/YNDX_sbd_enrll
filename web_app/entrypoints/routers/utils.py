from model import OfferAndCategory

from datetime import datetime


def node_create(data: dict, date: str) -> OfferAndCategory:
    """
    Creating node from the json data

    :param data: from the request body
    :param date: updateDate
    :return: node object
    """
    if data['type'] not in ["CATEGORY", "OFFER"]:  # check the correctness of category's name
        raise TypeError

    # because Python's library "datetime" does not understand "Z" notation (about the time zones)
    date = date.replace("Z", "+00:00")

    try:  # validate date format
        datetime.fromisoformat(date)
    except Exception:
        raise ValueError

    node = OfferAndCategory(
        uid=data['id'],
        name=data['name'],
        type=data['type'],
        date=date
    )

    if 'parentId' in data.keys():
        # check if node has a parent, if not - it will get base parent
        node.add_parent(data['parentId'] if data['parentId'] else '-1')

    if 'price' in data.keys():
        # check the correctness of a price format (type "int" was checked in importUnitParser applying)
        if data['price'] <= 0:
            raise ValueError
        node.add_price(data['price'])

    if node.type == "CATEGORY" and "price" in data.keys():
        # "CATEGORY" type can not have a user-defined price
        raise AttributeError

    if node.type == "OFFER" and "price" not in data.keys():
        # but "OFFER" type should have price field
        raise AttributeError

    return node
