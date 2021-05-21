#!/usr/bin/python3
import logging
import argparse
from aiohttp import web
from App.Views import routes
from App.Logger import AccessLogger


def parse():
    parser = argparse.ArgumentParser(description='PMZ (PROJECT: MAZE SOLVER)')
    parser.add_argument('-i', '--ip', type=str, help='Direccion en donde espera conexiones nuevas', default=['0.0.0.0', '::'])
    parser.add_argument('-p', '--port', type=int, help='Puerto en donde espera conexiones nuevas', default=80)
    args = vars(parser.parse_args())
    return args


args = parse()
app = web.Application()
app.router.add_routes(routes)
logger = logging.Logger("Custom")
logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=args['port'], host=args['ip'], access_log_class=AccessLogger)
