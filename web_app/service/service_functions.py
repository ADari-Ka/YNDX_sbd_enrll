"""Service layer for accessing to repository"""

from adapters import repositories

from typing import List
from model import OfferAndCategory, History

from datetime import datetime
import re


UUID_RE = r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$"


def import_node(node: OfferAndCategory, repo: repositories.AbstractRepository):
    if not re.match(UUID_RE, node.uid):  # validate UUID format
        raise ValueError

    repo.import_nodes(node)


def delete_node(node_id: str, repo: repositories.AbstractRepository):
    if not re.match(UUID_RE, node_id):  # validate UUID format
        raise ValueError

    repo.delete(node_id)


def get_node(node_id: str, repo: repositories.AbstractRepository):
    if not re.match(UUID_RE, node_id):  # validate UUID format
        raise ValueError

    node = repo.get(node_id)

    return node


def get_sales(date: str, repo: repositories.AbstractRepository) -> List[OfferAndCategory]:
    try:  # validate date format
        date_entity = datetime.fromisoformat(date.replace('Z', '+00:00'))
    except Exception:
        raise ValueError

    return repo.get_sales(date_entity)


def node_statistic(node_id, dates, repo: repositories.AbstractRepository) -> List[History]:
    if all(dates):
        try:  # validate date format
            date_start_entity = datetime.fromisoformat(dates[0].replace('Z', '+00:00'))
            date_end_entity = datetime.fromisoformat(dates[1].replace('Z', '+00:00'))
        except Exception:
            raise ValueError

        return repo.get_statistic(node_id, date_start_entity, date_end_entity)
    else:
        return repo.get_statistic(node_id)
