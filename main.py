#!/bin/python
##
##
##

import re
import sys, os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import convertion_controller

if len(sys.argv) != 2:
    print("[-] No se introdujo la ruta absoluta del recurso csv")
    exit(1)

CSV_FILE_NAME = sys.argv[1]

if not re.match(r'^/', CSV_FILE_NAME):
    print(f"[-] El argumento {CSV_FILE_NAME} no es una ruta absoluta")
    exit(1)

if not os.path.isfile(CSV_FILE_NAME):
    print(f"[-] No existe el recurso {CSV_FILE_NAME}")
    exit(2)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(convertion_controller.router)

if __name__ == "__main__":
    # uvicorn.run(app, host = "0.0.0.0", port=5000, log_level="info", ssl_keyfile = "certificates/private.key", ssl_certfile = "certificates/certchain.pem")
    uvicorn.run(app, host = "0.0.0.0", port=5000, log_level="info")

