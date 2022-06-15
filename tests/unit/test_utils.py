import pytest

from web_app.model import OfferAndCategory
from web_app.entrypoints.routers import utils


def test_creating_category_correct():
    data = {
        "type": "CATEGORY",
        "name": "Test",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "parentId": None
    }
    date = '2022-02-02T12:00:00.000Z'

    node = utils.node_create(data, date)

    assert type(node) == OfferAndCategory


def test_creating_offer_correct():
    data = {
        "type": "OFFER",
        "name": "Test",
        "id": "863e1a7a-1304-42ae-943b-179184c077e3",
        "price": 10,
        "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"
    }
    date = '2022-02-02T12:00:00.000Z'

    node = utils.node_create(data, date)

    assert type(node) == OfferAndCategory


def test_creating_node_wrong_type():
    data = {
        "type": "WRONG",
        "name": "Test",
        "id": "863e1a7a-1304-42ae-943b-179184c077e3",
    }
    date = '2022-02-02T12:00:00.000Z'

    try:
        utils.node_create(data, date)
    except TypeError:
        assert True


def test_creating_node_wrong_date():
    data = {
        "type": "CATEGORY",
        "name": "Test",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    }
    date = '31.12.2020'

    try:
        utils.node_create(data, date)
    except ValueError:
        assert True


def test_creating_offer_without_price():
    data = {
        "type": "OFFER",
        "name": "Test",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
    }
    date = '2022-01-01'

    try:
        utils.node_create(data, date)
    except AttributeError:
        assert True


def test_creating_offer_with_wrong_price():
    data = {
        "type": "OFFER",
        "name": "Test",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "price": -48
    }
    date = '2022-01-01'

    try:
        utils.node_create(data, date)
    except ValueError:
        assert True


def test_creating_category_with_price():
    data = {
        "type": "OFFER",
        "name": "Test",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "price": 32
    }
    date = '2022-01-01'

    try:
        utils.node_create(data, date)
    except AttributeError:
        assert True
