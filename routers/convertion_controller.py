#!/bin/python

import re
import time

from convertion import Convertion
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
    son usados como parámetros del script bash.
    @return #this.#show<
    """

    query = query.strip()

    if query == "": # Caso de uso no hay cadena -> optiene los servers por default
        return show(request)

    servers = None
    hour = None
    day = None
  
    for predicate in re.split(";", query):
        predicate = predicate.strip()

        if re.search('^ ?\\w+$', predicate): # caso de uso "1 server de hoy"
            servers = [predicate]
            continue 

        if  re.search('^ ?servers=\\w+(, ?\\w+)*$', predicate): # caso de uso "varios servers de hoy"
            servers = re.split(",", re.split("=", predicate)[1])
            continue
            
        if  re.search('^ ?hour=\\d+\\:\\d+$', predicate): # caso de uso "1 server a cierta hora"
            hour = re.split("=", predicate)[1]

            try:
                time.strptime(hour, '%H:%M')
            except ValueError:
                return show(request, query, f"Formato de HORA no válido ( {predicate} )")

            continue

        if  re.search('^ ?when=\\d+\\/\\d+/\\d+$', predicate): # caso de uso "1 server a cierta hora"
            day = re.split("=", predicate)[1]

            try:
                time.strptime(day, '%d/%m/%Y')
            except ValueError:
                return show(request, query, f"Formato de FECHA no válido ( {predicate} )")

            continue

        return show(request, query, f"Revisa el predicado '{predicate}'")

    if servers is None:
        return show(request, query, "Debes de agregar al menos el nombre de un server")        
    
    if hour is None and day is None:
        print("caso 1")

    if hour and day is None:
        print("caso 2")

    if hour is None and day:
        print("caso 3")

    if hour and day:
        print("caso 4")


    return show(request, query)

