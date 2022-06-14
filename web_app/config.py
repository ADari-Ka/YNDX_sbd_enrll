from adapters.repositories import AbstractRepository, SQLalchemyRepository


class AbstractSettings:
    mode_name: str
    _repository: AbstractRepository

    app_url: str

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str


class ProductionSettings(AbstractSettings):
    app_url = '0.0.0.0:8080'

    db_name = 'yndxe'  # idk how to make dependence between config and docker-compose files
    db_user = 'adarika'
    db_password = 'imgoingtothebackendschool'
    db_host = 'postgres_db'
    db_port = '5432'

    def get_repository(self, session) -> SQLalchemyRepository:
        return SQLalchemyRepository(session)

    def get_postgres_uri(self):
        return 'postgresql://{}:{}@{}:{}/{}'.format(self.db_user, self.db_password,
                                                    self.db_host, self.db_port, self.db_name)


def get_settings() -> ProductionSettings:
    return ProductionSettings()
