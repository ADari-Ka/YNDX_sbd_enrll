from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

from adapters import orm

app = FastAPI()

settings = config.get_settings()

db_engine = create_engine(settings.get_postgres_uri())
get_session = sessionmaker(bind=db_engine)

orm.create_all(db_engine)
orm.configure_mappers()
orm.base_node_create(get_session())
