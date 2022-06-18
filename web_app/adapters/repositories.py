import abc
import datetime

from model import OfferAndCategory


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, **kwargs):
        raise NotImplementedError


class FakeRepository(AbstractRepository):
    def __init__(self):
        pass

    def get(self, **kwargs):
        pass

    def add(self):
        pass


class SQLalchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def get(self, node_id) -> OfferAndCategory:
        nodes = self.session.query(OfferAndCategory).filter_by(uid=node_id).all()
        if not nodes:
            raise LookupError

        return nodes[0]

    def get_sales(self, date: datetime.datetime):
        result = []

        nodes = self.session.query(OfferAndCategory).filter_by(type="OFFER").all()
        for node in nodes:
            if date + datetime.timedelta(days=-1) <= datetime.datetime.fromisoformat(node.date) <= date:
                result.append(node)

        return result

    def add(self):
        pass

    def import_nodes(self, node):
        parent = None
        if node.parentId:
            parent_exists = self.session.query(OfferAndCategory).filter_by(uid=node.parentId).all()

            if parent_exists:
                parent = parent_exists[0]

            if parent.type == "OFFER":
                raise AttributeError

        existed_ = self.session.query(OfferAndCategory).filter_by(uid=node.uid).all()
        if existed_:
            existed_node = existed_[0]
            if existed_node.type != node.type:
                raise AttributeError
            # if existed_node.parentId == -1 and node.parentId:
                # self.session.query(OfferAndCategory).filter(uid=node.parentId).one().remove_child(node)

            existed_node = existed_node + node
        else:
            self.session.add(node)

        if parent:
            # node.parents.append(parent)
            parent.children.append(node)
            # parent.add_child(node)

    def delete(self, node_id):
        nodes = self.session.query(OfferAndCategory).filter_by(uid=node_id).all()
        if not nodes:
            raise LookupError

        current_node = nodes[0]

        # children = self.session.query(OfferAndCategory).filter_by(parentId=node_id).all()

        if current_node.children:
            for node_uid in current_node.children:
                if self.session.query(OfferAndCategory).filter_by(parentId=node_uid).all():
                    self.delete(node_uid)
                node = self.session.query(OfferAndCategory).filter_by(uid=node_uid).one()
                self.session.delete(node)

        # if current_node.parentId:
        #     self.session.query(OfferAndCategory).filter(uid=current_node.parentId).one().remove_child(current_node)

        self.session.delete(current_node)
