from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/nodes")


@router.post("/imports")
async def import_nodes(request: Request):
    pass
