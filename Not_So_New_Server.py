from aiohttp import web
import asyncio
import argparse


def parse():
    parser = argparse.ArgumentParser(description='PMZ (PROJECT: MAZE SOLVER)')
    parser.add_argument('-i', '--ip', type=str, help='Direccion en donde espera conexiones nuevas', default=['0.0.0.0', '::'])
    parser.add_argument('-p', '--port', type=int, help='Puerto en donde espera conexiones nuevas', default=80)

    args = vars(parser.parse_args())

    return args


class Server():

    async def handler(self, request):
        if request.path == '/':
            file = '/index.html'
        else:
            file = request.path
        return web.FileResponse(path='.'+file, status=200)

    async def main(self):
        server = web.Server(self.handler)
        web.Server()
        runner = web.ServerRunner(server)
        await runner.setup()
        site = web.TCPSite(runner=runner, host=args['ip'], port=args['port'], reuse_address=True)
        await site.start()
        if type(args['ip']) is list:
            for ip in args['ip']:
                print(f"======= Serving on http://{ip}:{args['port']}/ ======")
        else:
            print(f"======= Serving on http://{args['ip']}:{args['port']}/ ======")
        await asyncio.sleep(100*3600)


if __name__ == '__main__':
    args = parse()
    loop = asyncio.get_event_loop()
    server = Server()
    try:
        loop.run_until_complete(server.main())
    except KeyboardInterrupt:
        pass
    loop.close()
