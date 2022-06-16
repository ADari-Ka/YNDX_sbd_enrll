import abc

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

    def get(self):
        pass

    def add(self):
        pass

    def import_nodes(self, node):
        if node.parentId and \
                self.session.query(OfferAndCategory).filter_by(uid=node.parentId).one().type == "OFFER":
            raise AttributeError

        existed_ = self.session.query(OfferAndCategory).filter_by(uid=node.uid).all()
        if existed_:
            existed_node = existed_[0]
            existed_node = existed_node + node
        else:
            self.session.add(node)

    def delete(self, node_id):
        nodes = self.session.query(OfferAndCategory).filter_by(uid=node_id).all()
        if not nodes:
            raise LookupError

        current_node = nodes[0]

        children = self.session.query(OfferAndCategory).filter_by(parentId=node_id).all()

        for node in children:
            if self.session.query(OfferAndCategory).filter_by(parentId=node.uid).all():
                self.delete(node.uid)
            self.session.delete(node)

        self.session.delete(current_node)
