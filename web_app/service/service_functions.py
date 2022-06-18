from adapters import repositories

from datetime import datetime
import re


UUID_RE = r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$"


def import_node(node, repo: repositories.AbstractRepository):
    if not re.match(UUID_RE, node.uid):
        raise ValueError

    repo.import_nodes(node)


def delete_node(node_id: str, repo: repositories.AbstractRepository):
    if not re.match(UUID_RE, node_id):
        raise ValueError

    repo.delete(node_id)


def get_node(node_id: str, repo: repositories.AbstractRepository):
    if not re.match(UUID_RE, node_id):
        raise ValueError

    node = repo.get(node_id)

    return node


def get_sales(date: str, repo: repositories.AbstractRepository):
    try:
        date_entity = datetime.fromisoformat(date.replace('Z', '+00:00'))
    except Exception:
        raise ValueError

    return repo.get_sales(date_entity)


def node_statistic(node_id, repo: repositories.AbstractRepository):
    pass
