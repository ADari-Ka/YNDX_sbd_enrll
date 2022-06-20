from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, relationship, backref

from model import OfferAndCategory, History

mapper_registry = registry()

# table of History class
history_table = Table(
    "history",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("uid", String, nullable=False),
    Column("name", String, nullable=False),
    Column("parentId", String),
    Column("type", String, nullable=False),
    Column("date", String, nullable=False),
    Column("price", Integer)
)

# table of Node class; self-referenced by parent-children fields
node_table = Table(
    "node",
    mapper_registry.metadata,
    Column("uid", String, primary_key=True),
    Column("name", String, nullable=False),
    Column("date", String, nullable=False),
    Column("parentId", String, ForeignKey("node.uid")),
    Column("type", String),
    Column("price", Integer)
)


def configure_mappers():
    """
    Create mappers for domain models

    :return:
    """
    if not mapper_registry.mappers:  #
        node_mapper = mapper_registry.map_imperatively(OfferAndCategory,
                                                       node_table,
                                                       properties={
                                                           "children": relationship(
                                                               OfferAndCategory,
                                                               backref=backref("parent", remote_side=[node_table.c.uid])
                                                           )
                                                       }
                                                       )
        history_mapper = mapper_registry.map_imperatively(History, history_table)


def create_all(db_engine):
    """
    Creates tables in DataBase by registry metadata

    :param db_engine:
    :return:
    """
    mapper_registry.metadata.create_all(bind=db_engine)


def base_node_create(session):
    """
    Create base parent node to avoid inserting errors

    :param session: DataBase session for managing data
    :return:
    """
    if session.query(OfferAndCategory).filter_by(uid="-1").all():
        return

    base_node = OfferAndCategory(
        uid="-1",
        name="Base Node Parent Entity",
        type="BASE",
        date="1970-01-01T12:00:00.000+00:00"
    )

    session.add(base_node)
    session.commit()
