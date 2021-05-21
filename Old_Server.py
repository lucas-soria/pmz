#!/usr/bin/python3
import argparse
import asyncio
import pathlib
from Maze import Maze
from Table import Table


class ArgsError(Exception):
    pass


class DirectoryError(Exception):
    pass


def parse():
    parser = argparse.ArgumentParser(description='PMZ (PROJECT: MAZE SOLVER)')
    parser.add_argument('-i', '--ip', type=str, help='Direccion en donde espera conexiones nuevas', default=['0.0.0.0', '::'])
    parser.add_argument('-p', '--port', type=int, help='Puerto en donde espera conexiones nuevas', default=80)

    args = vars(parser.parse_args())

    return args


async def handler(reader, writer):
    data = b''
    while True:
        request = await reader.read(1024)
        data += request
        if len(request) < 1024:
            break
    try:
        data_splitted = data.decode().splitlines()
        encabezado_request = ''
        if data_splitted != []:
            encabezado_request = data_splitted[0]
        else:
            encabezado_request = 'Keep Alive'
        if encabezado_request.split(' ')[0] == 'GET':
            archivo = encabezado_request.split(' ')[1]
            await manejar_archivo(archivo, writer)
        elif encabezado_request.split(' ')[0] == 'POST':
            maze = data.decode().split('------WebKitFormBoundary')[1].split('\n\r\n')[1]
            print(maze)
            maze = Maze(maze)
            solution = maze.solve()
            print(maze.tree)
            print(maze.path)
            web = Table(maze.maze, solution)
            site_generated = bytearray(web.generate_html(), 'utf-8')
            pathsize = len(site_generated)
            await encabezado("OK", "html", pathsize, writer)
            writer.write(site_generated)
    except Exception:
        print('error')
        print(Exception.with_traceback())
    finally:
        client = writer.get_extra_info('peername')[0]
        try:
            await writer.drain()
        except ConnectionResetError:
            print(f"Connection lost with {client}")
        finally:
            writer.close()


async def run_server():
    print(f"Server running on: {args['ip']}:{args['port']}...")
    try:
        server = await asyncio.start_server(handler, args['ip'], args['port'])
    except (OverflowError, OSError):
        print("Error al iniciar el server")
        exit(-1)
    async with server:
        await server.serve_forever()


async def encabezado(cod, ext, pathsize, writer):
    extencion = {"txt": "text/plain",
                 "html": "text/html",
                 "css": "text/css",
                 "ico": "image/webp",
                 "js": "text/javascript", }
    codigo = {"OK": "200 OK",
              "NOT": "404 Not Found",
              "ERROR": "500 Internal Server Error"}
    encabezado_response = bytearray("HTTP/1.1 " + codigo[cod] + "\r\nContent-type: " + extencion[ext] +
                                    "\r\nContent-length: " + str(pathsize) + "\r\n\r\n", 'utf8')
    writer.write(encabezado_response)


async def manejar_archivo(archivo, writer):
    if archivo == '/':
        archivo = '/index.html'
        with open('./index.html', 'rb') as file:
            index = file.read()
        pathsize = len(index)
        await encabezado("OK", "html", pathsize, writer)
    else:
        archivo = str(pathlib.Path(__file__).parent.absolute()) + archivo
        try:
            if 'favicon' in archivo:
                archivo = str(pathlib.Path(__file__).parent.absolute()) + '/static/favicon.ico'
            file = open(archivo, "rb")
            cod = "OK"
        except FileNotFoundError:
            print('Error 404')
        except IsADirectoryError:
            raise DirectoryError("La direccion corresponde a un directorio")
        pathsize = pathlib.Path(archivo).stat().st_size
        await encabezado(cod, archivo.split(".")[-1], pathsize, writer)
    if archivo == '/index.html':
        writer.write(index)
    else:
        texto = file.read()
        while texto:
            writer.write(texto)
            texto = file.read()


if __name__ == "__main__":
    args = parse()
    asyncio.run(run_server())
