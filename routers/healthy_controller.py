#!/bin/python

import re
import time
import os

from convertion import Convertion
from datetime import date
from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/healthy",
    responses={404: {"description": "Página no encontrada"}},
)

convertion = Convertion()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def show(request: Request, servers : str = ""):
    """
    Vista del HC html
    """
    return templates.TemplateResponse('healthy.html', {
        'request': request,
        "healthylist": convertion.healthy_list("srmttilm2mxr302", True),
        "servers": "srmttilm2mxr302"
    })
