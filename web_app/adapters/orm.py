from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import registry, relationship, backref

from model import OfferAndCategory

mapper_registry = registry()


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
    if not mapper_registry.mappers:
        node_mapper = mapper_registry.map_imperatively(OfferAndCategory,
                                                       node_table,
                                                       properties={
                                                           "children": relationship(
                                                               OfferAndCategory,
                                                               backref=backref("parents", remote_side=[node_table.c.uid])
                                                           )
                                                       }
                                                       )


def create_all(db_engine):
    mapper_registry.metadata.create_all(bind=db_engine)


def base_node_create(session):
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
