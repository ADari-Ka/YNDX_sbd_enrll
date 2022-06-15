from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse

from fastapi_app import settings, get_session

from service import service_functions

from .units_parser import parser_match, ParseException
from .units_parser.parsers import importUnitParser, importParser

from .utils import node_create

from .responses_content import error400

router = APIRouter(prefix="/nodes")


@router.post("/imports")
async def import_nodes(request: Request):
    session = get_session()
    repo = settings.get_repository(session)

    request_data = request.json()
    try:
        await parser_match(request_data, importParser)
        await parser_match(request_data, importUnitParser)
    except ParseException:
        return JSONResponse(status_code=400, content=error400)

    try:
        for element in request_data['items']:
            node = node_create(element, request_data['updateDate'])
            service_functions.import_node(node, repo)
        return Response(status_code=200)
    except Exception:
        return JSONResponse(status_code=400, content=400)
    finally:
        session.commit()
