import abc
from typing import List, Union

import datetime

from model import OfferAndCategory, History


class AbstractRepository(abc.ABC):
    """Abstract class (like special tool) for managing data store"""
    @abc.abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, **kwargs):
        raise NotImplementedError


class FakeRepository(AbstractRepository):
    """
    This class exist only because it MIGHT help via testing.
    But it is useless due to enrollment deadline
    """
    def __init__(self):
        pass

    def get(self, **kwargs):
        pass

    def add(self):
        pass


class SQLalchemyRepository(AbstractRepository):
    """Special tool for handling data operations in DataBase"""

    def __init__(self, session):
        """Creating the DataBase session for operations"""
        self.session = session

    def get(self, node_id: str) -> OfferAndCategory:
        """
        Get data about node with specific ID

        :param node_id:
        :return: OfferAndCategory (node) object
        """
        nodes: List[OfferAndCategory] = self.session.query(OfferAndCategory).filter_by(uid=node_id).all()
        if not nodes:
            raise LookupError

        return nodes[0]

    def get_sales(self, date: datetime.datetime) -> List[OfferAndCategory]:
        """
        Get arrays of nodes with needed date

        :param date: date for searching nodes
        :return:
        """
        result = []

        nodes: List[OfferAndCategory] = self.session.query(OfferAndCategory).filter_by(type="OFFER").all()

        if not nodes:
            raise LookupError

        for node in nodes:
            if date + datetime.timedelta(days=-1) <= datetime.datetime.fromisoformat(node.date) <= date:
                result.append(node)

        return result

    def get_statistic(self, node_uid: str, date_start: datetime.datetime, date_end: datetime.datetime) \
            -> List[OfferAndCategory]:
        """
        Gets array with full history of updates (in given interval) of a certain node

        :param node_uid:
        :param date_start:
        :param date_end:
        :return:
        """
        result = []

        nodes: List[History] = self.session.query(History).filter_by(uid=node_uid).all()

        if not nodes:
            raise LookupError

        for node in nodes:
            if date_start <= datetime.datetime.fromisoformat(node.date) < date_end:
                result.append(node)

        return result

    def add(self, node: OfferAndCategory):
        """
        Add history record to the DataBase with info of certain node

        :param node: node with data for recording
        :return:
        """

        price_t = node.get_price()
        price = int(price_t[0] / price_t[1]) if price_t[0] and price_t[1] else 0

        history_record = History(
            uid=node.uid,
            name=node.name,
            parentId=node.parentId,
            type=node.type,
            price=price,
            date=node.date
        )
        self.session.add(history_record)

    def import_nodes(self, node: OfferAndCategory):
        parent: Union[None, OfferAndCategory] = None

        if node.parentId:
            # gets parent's node by id and do validation about type
            parent_exists = self.session.query(OfferAndCategory).filter_by(uid=node.parentId).all()

            if parent_exists:
                parent = parent_exists[0]

            if parent.type == "OFFER":
                raise AttributeError  # because parent's type can not be "OFFER"

        e_node = None
        existed_node: Union[OfferAndCategory, None] = \
            self.session.query(OfferAndCategory).filter_by(uid=node.uid).all()
        # gets node if it exists and update info in the NODE table in DataBase by id

        if existed_node:
            e_node = existed_node[0]
            if e_node.type != node.type:
                raise AttributeError  # because we can not change node's type

            e_node + node
            self.session.add(e_node)
        else:
            self.session.add(node)

        self.add(node)

        if parent:  # manage relations
            parent.children.append(node if not e_node else e_node)
            parent.update_date(node.date)

    def delete(self, node_id: str):
        """
        Delete node from the DataBase and its history records

        :param node_id:
        :return:
        """
        nodes: List[OfferAndCategory] = self.session.query(OfferAndCategory).filter_by(uid=node_id).all()
        if not nodes:
            raise LookupError

        current_node: OfferAndCategory = nodes[0]

        if current_node.children:
            for node in current_node.children:
                if node.children:
                    self.delete(node.uid)
                self.session.delete(node)

        self.session.delete(current_node)

        history_records: List[History] = self.session.query(History).filter_by(uid=node_id).all()

        for record in history_records:
            self.session.delete(record)
