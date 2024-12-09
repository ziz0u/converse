#!/bin/python

import re
import time
import os

from convertion import Convertion
from datetime import date
from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    responses={404: {"description": "Página no encontrada"}},
)

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return RedirectResponse(url='/convertion')
