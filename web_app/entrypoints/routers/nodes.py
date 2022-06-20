from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from typing import Union

from fastapi_app import settings, get_session  # getting needed tools

from service import service_functions

# parser tools units
from .units_parser import parser_match, ParseException
from .units_parser.parsers import importUnitParser, importParser

from .utils import node_create

from .responses_content import error400, error404  # fast-access response contents

router = APIRouter()


@router.post("/imports")
async def import_nodes(request: Request):
    """Receive json data in request body and load it to the DataBase"""

    session = get_session()
    repo = settings.get_repository(session)

    request_data = await request.json()

    # validate request
    try:
        parser_match(request_data, importParser)
        parser_match(request_data, importUnitParser)
    except ParseException:
        return JSONResponse(status_code=400, content=error400)

    # creating node (with validation) and add it into the DataBase table
    try:
        for element in request_data['items']:
            node = node_create(element, request_data['updateDate'])  # validation while node creation
            service_functions.import_node(node, repo)
        session.commit()  # commit changes
        return Response(status_code=200)
    except Exception:  # exceptions occur because of validation process
        return JSONResponse(status_code=400, content=error400)
    finally:
        session.commit()


@router.delete('/delete/{id}')
async def delete_node(id: str):
    """
    Delete node in the DataBase

    :param id: node's id for finding it in the DataBase
    :return: JSONResponse
    """
    session = get_session()
    repo = settings.get_repository(session)

    try:
        service_functions.delete_node(id, repo)
        session.commit()
        return Response(status_code=200)
    except ValueError:  # validation error
        return JSONResponse(status_code=400, content=error400)
    except LookupError:
        return JSONResponse(status_code=404, content=error404)
    finally:
        session.commit()


@router.get('/nodes/{id}')
async def get_node(id: str):
    """
    Gets node's information (include children) from the DataBase

    :param id: node's id for finding it in the DataBase
    :return: JSONResponse
    """
    session = get_session()
    repo = settings.get_repository(session)

    try:
        node = service_functions.get_node(id, repo)
        return JSONResponse(status_code=200, content=node.to_dict())
    except ValueError:  # validation error
        return JSONResponse(status_code=400, content=error400)
    except LookupError:
        return JSONResponse(status_code=404, content=error404)


@router.get('/sales')
async def get_sales(date: Union[str, None] = None):
    """
    Gets array of nodes with type "OFFER" with proper date

    :param date: in ISO8601 format
    :return: JSONResponse
    """
    session = get_session()
    repo = settings.get_repository(session)

    if not date:
        return JSONResponse(status_code=400, content=error400)
    try:
        offers: list = service_functions.get_sales(date, repo)
        content = list(offer.to_dict(need_children=False) for offer in offers)
        return JSONResponse(status_code=200, content=content)
    except ValueError:  # validation error
        return JSONResponse(status_code=400, content=error400)


@router.get('/node/{id}/statistic')
async def get_statistic(id: str, dateStart: Union[str, None] = None, dateEnd: Union[str, None] = None):
    """
    Gets node's history

    :param id: node's id for finding it in the DataBase
    :param dateStart: for searching
    :param dateEnd: for searching
    :return: JSONResponse
    """
    session = get_session()
    repo = settings.get_repository(session)

    if not (dateStart and dateEnd):
        return JSONResponse(status_code=400, content=error400)

    try:
        data = service_functions.node_statistic(id, (dateStart, dateEnd), repo)
        return JSONResponse(status_code=200, content={"items": list(history_node.to_dict() for history_node in data)})
    except ValueError:  # validation error
        return JSONResponse(status_code=400, content=error404)
    except LookupError:
        return JSONResponse(status_code=404, content=error404)
