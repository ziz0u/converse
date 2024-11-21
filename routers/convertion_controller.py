#!/bin/python

import re
import time
import os

from convertion import Convertion
from datetime import date
from fastapi import APIRouter, HTTPException, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

router = APIRouter(
    prefix="/convertion",
    responses={404: {"description": "Página no encontrada"}},
)

convertion = Convertion()
templates = Jinja2Templates(directory="templates")

def regex_search(text, regexp):
    return re.search(regexp, text) 

templates.env.filters['regex_search'] = regex_search

class QueryServer(BaseModel):
    isSpecificDay : bool = False
    day : str = "day"
    start_hour : str = ""
    end_hour : str = ""
    servers : str = ""
    message_error: str = ""

@router.get("/", response_class=HTMLResponse)
def show(request: Request, query: QueryServer = QueryServer()):
    """
    Conviente el recurso csv a un formato html
    """
    return templates.TemplateResponse('convertion.html', {
        'request': request, 
        "csvlist": convertion.to_list(),
        "healthylist": convertion.healthy_list(query.servers),
        "isSpecificDay": query.isSpecificDay,
        "day": query.day,
        "start_hour": query.start_hour,
        "end_hour": query.end_hour,
        "servers": query.servers,
        "message_error": query.message_error
    })

@router.post("/analyze", response_class=HTMLResponse)
def analize_with_script_bash(request: Request, query: QueryServer = QueryServer()):
    """
    Este wey recaba parámetros de fecha hora y/o nombre del servidor, los params
    son usados como parámetros del script bash (ansible-playbook).

    @return #this.#show
    """
    query.servers = query.servers.strip()
    query.message_error = "No has agregado un servidor para analizar"

    if query.servers == "":
        return show(request, query)

    if not query.isSpecificDay or query.day == "day":
        query.day = date.today().strftime('%d')

    this_month = date.today().strftime('%m')
    this_year = date.today().strftime('%Y')

    try:
        time.strptime(f"{query.day}/{this_month}/{this_year}", '%d/%m/%Y')
    except ValueError:
        query.message_error = f"Día del mes no válido ( {day} )" 
        return show(request, query)


    hours = [f"{query.start_hour}:00", f"{query.end_hour}:00"]

    if query.start_hour == "" and query.end_hour == "":
        hours = ["00:00:00", "23:59:59"]

    try:
        time.strptime(hours[0], '%H:%M:%S')
        time.strptime(hours[1], '%H:%M:%S')
    except ValueError:
        query.message_error = f"Formato de HORAS no válido ( {start_hour} - {end_hour} )" 
        return show(request, query)

    os.system(f"""
        echo "ansible-playbook -u user -s \\
          Vulnerabilities/analysisForIncidents.sh -d {query.day} {hours[0]} {hours[1]} \\
          -o logfile.csv -i {query.servers}"
    """)


    return show(request, query)

