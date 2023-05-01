#!/usr/bin/env python3

from flask import Flask, request

from controller import ReportClientController
from controller import ReportServerController
from controller import ReportGeneralController

from utils import config


conf = config.config_from_cmdline()

app = Flask(__name__)


@app.get('/api/report/client')
def get_client_report():
    req = request.json
    controller = ReportClientController(req)
    res = controller.get_report()

    return res


@app.get('/api/report/server')
def get_server_report():
    req = request.json
    controller = ReportServerController(req)
    res = controller.get_report()

    return res


@app.get('/api/report/general')
def get_general_report():
    req = request.json
    controller = ReportGeneralController(req)
    res = controller.get_report()

    return res


app.run(
    host=conf['addr'],
    port=conf['port']
)
