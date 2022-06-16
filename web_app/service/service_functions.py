from adapters import repositories

import re


UUID_RE = r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$"


def import_node(node, repo: repositories.AbstractRepository):
    if not re.match(UUID_RE, node.uid):
        raise ValueError

    repo.import_nodes(node)


def delete_node(node_id, repo: repositories.AbstractRepository):
    if not re.match(UUID_RE, node_id):
        raise ValueError

    repo.delete(node_id)


def get_node(node_id, repo: repositories.AbstractRepository):
    if not re.match(UUID_RE, node_id):
        raise ValueError

    return repo.get(node_id)


def get_sales(repo: repositories.AbstractRepository):
    pass


def node_statistic(node_id, repo: repositories.AbstractRepository):
    pass
