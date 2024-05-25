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
    prefix="/convertion",
    responses={404: {"description": "Página no encontrada"}},
)

convertion = Convertion()
templates = Jinja2Templates(directory="templates")

def regex_search(text, regexp):
    return re.search(regexp, text) 

templates.env.filters['regex_search'] = regex_search


@router.get("/", response_class=HTMLResponse)
def show(request: Request, isSpecificDay : bool = False, day : str = "day",
        start_hour : str = "", end_hour : str = "", servers : str = "", message_error: str = ""):
    """
    Conviente el recurso csv a un formato html
    """
    return templates.TemplateResponse('convertion.html', {
        'request': request, 
        "csvlist": convertion.to_list(),
        "healthylist": convertion.healthy_list(servers),
        "isSpecificDay": isSpecificDay,
        "day": day,
        "start_hour": start_hour,
        "end_hour": end_hour,
        "servers": servers,
        "message_error": message_error
    })


@router.get("/analyze", response_class=HTMLResponse)
def analize_with_script_bash(request: Request, isSpecificDay : bool = False, day : str = "day",
        start_hour : str = "", end_hour : str = "", servers : str = ""):
    """
    Este wey recaba parámetros de fecha hora y/o nombre del servidor, los params
    son usados como parámetros del script bash (ansible-playbook).

    @return #this.#show
    """
    servers = servers.strip()

    if servers == "":
        return show(request, isSpecificDay, day, start_hour, end_hour, servers, "No has agregado un servidor para analizar")

    if not isSpecificDay or day == "day":
        day = date.today().strftime('%d')

    this_month = date.today().strftime('%m')
    this_year = date.today().strftime('%Y')

    try:
        time.strptime(f"{day}/{this_month}/{this_year}", '%d/%m/%Y')
    except ValueError:
        return show(request, isSpecificDay, day, start_hour, end_hour, servers,
                f"Día del mes no válido ( {day} )")


    hours = [f"{start_hour}:00", f"{end_hour}:00"]

    if start_hour == "" and end_hour == "":
        hours = ["00:00:00", "23:59:59"]

    try:
        time.strptime(hours[0], '%H:%M:%S')
        time.strptime(hours[1], '%H:%M:%S')
    except ValueError:
        return show(request, isSpecificDay, day, start_hour, end_hour, servers,
                f"Formato de HORAS no válido ( {start_hour} - {end_hour} )")

    os.system(f"""
        echo "ansible-playbook -u user -s \\
          Vulnerabilities/analysisForIncidents.sh -d {day} {hours[0]} {hours[1]} \\
          -o logfile.csv -i {servers}"
    """)


    return show(request, isSpecificDay, day, start_hour, end_hour, servers)

