#!/bin/python
##
##
##

import re
import sys, os
import uvicorn
from uvicorn.config import LOGGING_CONFIG
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import convertion_controller, healthy_controller, index_controller

if len(sys.argv) != 3:
    print("[-] Verifica la cantidad de parámetros, 1 (csv con lusta de servers) 2 (csv con lista de healthchecks)")
    exit(1)

CSV_FILE_NAME = sys.argv[1]

if not re.match(r'^/', CSV_FILE_NAME):
    print(f"[-] El 1er argumento {CSV_FILE_NAME} no es una ruta absoluta")
    exit(1)

if not os.path.isfile(CSV_FILE_NAME):
    print(f"[-] No existe el recurso {CSV_FILE_NAME}")
    exit(2)

HEALTHY_FILE = sys.argv[2]

if not re.match(r'^/', HEALTHY_FILE):
    print(f"[-] El 2o argumento {HEALTHY_FILE} no es una ruta absoluta")
    exit(1)

if not os.path.isfile(HEALTHY_FILE):
    print(f"[-] No existe el recurso {HEALTHY_FILE}")
    exit(2)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/fonts", StaticFiles(directory="static/fonts"), name="fonts")
app.include_router(convertion_controller.router)
app.include_router(healthy_controller.router)
app.include_router(index_controller.router)

if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(asctime)s %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    uvicorn.run("main:app", host = "0.0.0.0", port=5000, log_level="info", ssl_keyfile="certificates/private.key", ssl_certfile="certificates/certchain.pem")
    #uvicorn.run(app, host = "0.0.0.0", port=5000, log_level="info")
