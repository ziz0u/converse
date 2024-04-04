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
    return templates.TemplateResponse('convertion.html', {
        'request': request, 
        "csvlist": convertion.to_list()
    })

@router.post("/analyze", response_class=HTMLResponse)
def analize_with_script_bash(request: Request):
    """
    Este wey recaba parametros de fecha hora y/o nombre del servidor, los params
    son usados como parametros del script bash.
    @return #this.#show
    """
    # TODO: invocar funcion bash
    return show(request)

