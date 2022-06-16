import pytest
import requests

URL = "http://web_app:8080"


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
                "price": 10
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 200


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


def test_update_category_import():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df9"
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    requests.post(URL + '/imports', json=data)

    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269dfa"
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    assert r.status_code == 200


def test_delete_node_correct():
    r = requests.delete(URL + '/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df1')

    assert r.status_code == 200


def test_delete_node_wrong_format():
    r = requests.delete(URL + '/delete/37')

    assert r.status_code == 400


def test_delete_node_404():
    r = requests.delete(URL + '/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269da1')

    assert r.status_code == 404


def test_delete_node_correct_cascade():
    data = {
        "items": [
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3"
            },
            {
                "type": "CATEGORY",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df3"
            },
            {
                "type": "OFFER",
                "name": "Test",
                "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df5",
                "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df4",
                "price": 10
            }
        ],
        "updateDate":
            "2022-02-02T12:00:00.000Z"
    }

    r = requests.post(URL + '/imports', json=data)

    r = requests.delete(URL + '/delete/069cb8d7-bbdd-47d3-ad8f-82ef4c269df3')

    assert r.status_code == 200
