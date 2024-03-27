#!/bin/python

from convertion import Convertion
from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/convertion",
    responses={404: {"description": "Página no encontrada"}},
)

convertion = Convertion()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def show(request: Request):
    """
    Conviente el recurso csv a un formato html
    """

    return templates.TemplateResponse(
        request=request, name="convertion.html", context={"csvlist": convertion.to_list()}
    )

    return { "message": "ok"}