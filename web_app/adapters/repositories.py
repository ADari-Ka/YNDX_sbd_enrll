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

    def delete(self):
        pass
