#!/usr/bin/python3
import argparse
import asyncio


class ArgsError(Exception):
    pass


class DirectoryError(Exception):
    pass


def parse():
    parser = argparse.ArgumentParser(description='PMZ (PROJECT: MAZE SOLVER)')
    parser.add_argument('-i', '--ip', type=int, help='Direccion en donde espera conexiones nuevas', default=['0.0.0.0', '::'])
    parser.add_argument('-p', '--port', type=int, help='Puerto en donde espera conexiones nuevas', default=80)

    args = vars(parser.parse_args())

    return args


async def handler(reader, writer):
    data = await reader.read()
    try:
        data = data.decode().splitlines()
        encabezado_request = ''
        if data != []:
            encabezado_request = data[0]
        else:
            encabezado_request = 'Keep Alive'
        encabezado_request_dividido = encabezado_request.split(' ')
        if encabezado_request_dividido[0] == 'GET':
            archivo = encabezado_request_dividido[1]
            await manejar_archivo(archivo, writer)
        if encabezado_request_dividido[0] == 'POST':
            request = data
            print(request)
    except Exception:
        archivo = "/500error.html"
        encabezado_request += "\tERROR"
        await manejar_archivo(archivo, writer)
    finally:
        client = writer.get_extra_info('peername')[0]
        try:
            await writer.drain()
        except ConnectionResetError:
            print(f"Conection lost with {client}")
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
                 "html": "text/html"}
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
    if archivo == '/index.html':
        writer.write(index)


if __name__ == "__main__":
    args = parse()
    asyncio.run(run_server())
