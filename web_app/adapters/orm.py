from sqlalchemy import Table, Column, Integer, String, ARRAY
from sqlalchemy.orm import registry

from model import OfferAndCategory

mapper_registry = registry()

offer_and_category_table = Table(
    "offer_and_category",
    mapper_registry.metadata,
    Column("uid", String, primary_key=True,),
    Column("name", String, nullable=False),
    Column("_date", String, nullable=False),
    Column("parentId", String, nullable=True),
    Column("type", String),
    Column("price", Integer),
    Column("children", ARRAY(String))
)


def configure_mappers():
    if not mapper_registry.mappers:
        mapper_registry.map_imperatively(OfferAndCategory, offer_and_category_table)


def create_all(db_engine):
    mapper_registry.metadata.create_all(bind=db_engine)
