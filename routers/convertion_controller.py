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


@router.get("/", response_class=HTMLResponse)
def show(request: Request, query: str = "", message_error: str = ""):
    """
    Conviente el recurso csv a un formato html
    """

    return templates.TemplateResponse('convertion.html', {
        'request': request, 
        "csvlist": convertion.to_list(),
        "query": query,
        "message_error": message_error
    })


@router.get("/analyze", response_class=HTMLResponse)
def analize_with_script_bash(request: Request, query: str):
    """
    Este wey recaba parámetros de fecha hora y/o nombre del servidor, los params
    son usados como parámetros del script bash (ansible-playbook).

    El formato de una consulta puede ser:

    server1
    servers=server1,server2
    time=HH:mm HH:mm
    year=dd

    O convinacion de las anteriores separadas por ";", por ejemplo:
    servers=server1,server2; day=11; time=00:00 23:00
    server2; day=01
    servers=server1,server2,s3; time=00:00        


    @return #this.#show
    """

    query = query.strip()

    if query == "": # Caso de uso no hay cadena -> optiene los servers por default
        return show(request)

    hours[0] = "00:00:00"
    hours[1] = "23:59:59"
    day = date.today().strftime('%d')
  
    for predicate in re.split(";", query):
        predicate = predicate.strip()

        if re.search('^ ?\\w+$', predicate):
            servers = [predicate]
            continue 

        if  re.search('^ ?servers=\\w+(, ?\\w+)*$', predicate):
            servers = re.split(",", re.split("=", predicate)[1])
            continue
            
        if  re.search('^ ?time=\\d+\\:\\d+ d+\\:\\d+$', predicate):
            hours = re.split(" ", re.split("=", predicate)[1])

            try:
                time.strptime(hours[0], '%H:%M')
                time.strptime(hours[1], '%H:%M')
            except ValueError:
                return show(request, query, f"Formato de HORAS no válido ( {predicate} )")

            continue

        if  re.search('^ ?day=\\d+$', predicate):
            day = re.split("=", predicate)[1]
            this_month = date.today().strftime('%m')
            this_year = date.today().strftime('%Y')

            try:
                time.strptime(f"{today}/{this_month}/{this_year}", '%d/%m/%Y')
            except ValueError:
                return show(request, query, f"Día del mes no válido ( {predicate} )")

            hours[0] = f"{hours[0]}:00"
            hours[1] = f"{hours[1]}:00"

            continue

        return show(request, query, f"Revisa el predicado '{predicate}'")

    if servers is None:
        return show(request, query, "Debes de agregar al menos el nombre de un server (servers=<s1>,<s2>,<sN>)")

    os.system(f"""
        ansible-playbook -u user -s \\
          Vulnerabilities/analysisForIncidents.sh -d {day} {hours[0]} {hours[1]} \\
          -o logfile.csv -i {",".join(servers)}
    """)


    return show(request, query)

