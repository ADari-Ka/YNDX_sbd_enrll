import pytest
import requests

URL = "http://web_app:80"


def test_connection():
    requests.get(URL)


""" BEGIN OF THE MAIN TEST BLOCK """


def test_new_category_import_correct():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 200


def test_get_empty_category_correct():
    r = requests.get(URL + '/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')

    expected = {
        "type": "CATEGORY",
        "name": "Test",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "date": "2022-02-02T12:00:00.000+00:00",
        "price": None,
        "parentId": None,
        "children": None
    }

    assert r.status_code == 200
    assert r.json() == expected


def test_delete_category_correct():
    r = requests.delete(URL + '/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')

    assert r.status_code == 200


def test_new_offer_import_correct():
    data = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "price": 89
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 200


def test_new_offer_and_category_import_correct():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3"
            },
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
                "price": 11
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 200


def test_get_category_with_child():
    r = requests.get(URL + '/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3')

    expected = {
        "type": "CATEGORY",
        "name": "Test",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
        "date": "2022-02-02T12:00:00.000+00:00",
        "price": 11,
        "parentId": None,
        "children": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
                "date": "2022-02-02T12:00:00.000+00:00",
                "price": 11,
                "children": None
            }
        ]
    }

    assert r.status_code == 200
    assert r.json() == expected


def test_update_category_import():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Test-Update",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3"
            }
        ],
        "updateDate":
            "2022-03-08T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 200


def test_get_updated_date_category_correct():
    r = requests.get(URL + '/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3')

    date_expected = '2022-03-08T12:00:00.000+00:00'

    assert r.status_code == 200
    assert r.json()["date"] == date_expected


def test_update_category_with_new_child():
    data = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
                "price": 55
            }
        ],
        "updateDate":
            "2022-04-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 200


def test_get_cascade():
    r = requests.get(URL + '/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3')

    expected = {
        "type": "CATEGORY",
        "name": "Test-Update",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3",
        "date": "2022-04-02T12:00:00.000+00:00",
        "price": 33,
        "parentId": None,
        "children": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
                "price": 11,
                "date": '2022-02-02T12:00:00.000+00:00',
                "children": None,
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3"
            },
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "price": 55,
                "date": '2022-04-02T12:00:00.000+00:00',
                "children": None,
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3"
            }
        ]
    }

    assert r.status_code == 200
    assert r.json() == expected


def test_get_history():
    r = requests.get(URL + '/node/069cb8d7-bbdd-47d3-ad8f-82ef4c269df2/statistic')

    expected = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "date": '2022-02-02T12:00:00.000+00:00',
                "price": 89,
                "parentId": None
            },
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "price": 55,
                "date": '2022-04-02T12:00:00.000+00:00',
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3"
            }
        ]
    }

    assert r.status_code == 200
    assert r.json() == expected, r.json()


def test_get_history_with_interval():
    r = requests.get(URL +
                     '/node/069cb8d7-bbdd-47d3-ad8f-82ef4c269df2/statistic?'
                     'dateStart=2022-01-02T12:00:00.000Z&'
                     'dateEnd=2022-03-02T12:00:00.000Z')

    expected = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "date": '2022-02-02T12:00:00.000+00:00',
                "price": 89,
                "parentId": None
            }
        ]
    }

    assert r.status_code == 200
    assert r.json() == expected


def test_get_sales():
    r = requests.get(URL + '/sales?date=2022-02-02T12:00:00.000Z')

    expected = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df2",
                "date": '2022-02-02T12:00:00.000+00:00',
                "price": 89,
                "parentId": None
            },
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
                "price": 11,
                "date": '2022-02-02T12:00:00.000+00:00',
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3"
            }
        ]
    }

    assert r.status_code == 200
    assert r.json() == expected


def test_delete_node_correct_cascade():
    r = requests.delete(URL + '/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3')

    assert r.status_code == 200


""" END OF MAIN BLOCK """


def test_sales_two_updates():
    data = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": 10,
            }
        ],
        "updateDate":
            "2022-02-02T11:10:00.000Z"
    }

    requests.post(URL + '/imports', json=data)

    data = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test-UPD",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": 11
            }
        ],
        "updateDate":
            "2022-02-02T11:30:00.000Z"
    }

    requests.post(URL + '/imports', json=data)

    expected = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test-UPD",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
                "price": 11,
                "parentId": None,
                "date": "2022-02-02T11:30:00.000+00:00"
            }
        ]
    }

    r = requests.get(URL + '/sales?date=2022-02-02T11:35:00.000Z')

    assert r.status_code == 200
    assert r.json() == expected

    requests.delete(URL + '/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')


def test_empty_sales():
    expected = {
        "items": []
    }

    r = requests.get(URL + '/sales?date=2022-02-02T12:00:00.000Z')

    assert r.status_code == 200
    assert r.json() == expected


def test_get_deleted_node():
    r = requests.get(URL + '/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df2')

    assert r.status_code == 404


def test_get_statistic_of_deleted_node():
    r = requests.get(URL + '/nodes/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3/statistic')

    assert r.status_code == 404


def test_get_statistic_of_deleted_node_with_wrong_dates():
    r = requests.get(URL + '/node/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3/statistic?dateStart=777&dateEnd=777')

    assert r.status_code == 400


def test_new_offer_without_price_import():
    data = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df5"
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 400
    assert r.json() == {"code": 400, "message": "Validation Failed"}


def test_new_offer_with_wrong_price_import():
    data = {
        "items": [
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df6",
                "price": -55
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 400
    assert r.json() == {"code": 400, "message": "Validation Failed"}


def test_new_category_with_price_import():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df7",
                "price": 37
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 400
    assert r.json() == {"code": 400, "message": "Validation Failed"}


def test_new_node_with_wrong_date_import():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df8"
            }
        ],
        "updateDate":
            "31 12 2020"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 400
    assert r.json() == {"code": 400, "message": "Validation Failed"}


def test_delete_node_wrong_format():
    r = requests.delete(URL + '/delete/37')

    assert r.status_code == 400


def test_delete_node_404():
    r = requests.delete(URL + '/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269da1')

    assert r.status_code == 404
