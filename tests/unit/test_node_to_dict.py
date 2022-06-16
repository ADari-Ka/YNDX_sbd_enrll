import pytest

from model import OfferAndCategory


def test_offer():
    node = OfferAndCategory(
        uid="3fa85f64-5717-4562-b3fc-2c963f66a333",
        name="Test",
        type="OFFER",
        date="2022-05-28T21:12:01.000+00:00"
    )

    node.add_price(76)

    expected = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66a333",
        "name": "Test",
        "type": "OFFER",
        "date": "2022-05-28T21:12:01+00:00",
        "price": 76,
        "parentId": None,
        "children": []
    }

    assert node.to_dict() == expected


def test_category_with_children():
    node0 = OfferAndCategory(
        uid="3fa85f64-5717-4562-b3fc-2c963f66a332",
        name="Test",
        type="CATEGORY",
        date="2022-05-28T21:12:01.000+00:00"
    )

    node1 = OfferAndCategory(
        uid="3fa85f64-5717-4562-b3fc-2c963f66a333",
        name="Test",
        type="OFFER",
        date="2022-05-28T21:12:01.000+00:00"
    )
    node1.add_price(76)
    node1.add_parent("3fa85f64-5717-4562-b3fc-2c963f66a332")

    node2 = OfferAndCategory(
        uid="3fa85f64-5717-4562-b3fc-2c963f66a334",
        name="Test",
        type="CATEGORY",
        date="2022-05-28T21:12:01.000+00:00"
    )
    node2.add_parent("3fa85f64-5717-4562-b3fc-2c963f66a332")

    node3 = OfferAndCategory(
        uid="3fa85f64-5717-4562-b3fc-2c963f66a335",
        name="Test",
        type="OFFER",
        date="2022-05-28T21:12:01.000+00:00"
    )
    node3.add_price(29)
    node3.add_parent("3fa85f64-5717-4562-b3fc-2c963f66a334")

    node4 = OfferAndCategory(
        uid="3fa85f64-5717-4562-b3fc-2c963f66a336",
        name="Test",
        type="OFFER",
        date="2022-05-28T21:12:01.000+00:00"
    )
    node4.add_price(13)
    node4.add_parent("3fa85f64-5717-4562-b3fc-2c963f66a334")

    node5 = OfferAndCategory(
        uid="3fa85f64-5717-4562-b3fc-2c963f66a337",
        name="Test",
        type="CATEGORY",
        date="2022-05-28T21:12:01.000+00:00"
    )
    node5.add_parent("3fa85f64-5717-4562-b3fc-2c963f66a334")

    node2.add_child(node3)
    node2.add_child(node4)
    node2.add_child(node5)

    node0.add_child(node1)
    node0.add_child(node2)

    expected = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66a332",
        "name": "Test",
        "type": "CATEGORY",
        "date": "2022-05-28T21:12:01+00:00",
        "price": 48,
        "parentId": None,
        "children": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a333",
                "name": "Test",
                "type": "OFFER",
                "date": "2022-05-28T21:12:01+00:00",
                "price": 76,
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a332",
                "children": []
            },
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66a334",
                "name": "Test",
                "type": "CATEGORY",
                "date": "2022-05-28T21:12:01+00:00",
                "price": 21,
                "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a332",
                "children": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66a335",
                        "name": "Test",
                        "type": "OFFER",
                        "date": "2022-05-28T21:12:01+00:00",
                        "price": 29,
                        "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a334",
                        "children": []
                    },
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66a336",
                        "name": "Test",
                        "type": "OFFER",
                        "date": "2022-05-28T21:12:01+00:00",
                        "price": 13,
                        "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a334",
                        "children": []
                    },
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66a337",
                        "name": "Test",
                        "type": "CATEGORY",
                        "date": "2022-05-28T21:12:01+00:00",
                        "price": None,
                        "parentId": "3fa85f64-5717-4562-b3fc-2c963f66a334",
                        "children": []
                    },

                ]
            }
        ]
    }
    res = node0.to_dict()

    assert res == expected
