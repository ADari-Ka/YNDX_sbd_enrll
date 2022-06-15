from adapters import repositories


def import_node(node, repo: repositories.AbstractRepository):
    repo.import_nodes(node)


def delete_node(entity, repo: repositories.AbstractRepository):
    pass


def get_node(node_id, repo: repositories.AbstractRepository):
    pass


def get_sales(repo: repositories.AbstractRepository):
    pass


def node_statistic(node_id, repo: repositories.AbstractRepository):
    pass

