from aiohttp.abc import AbstractAccessLogger


class AccessLogger(AbstractAccessLogger):

    def log(self, request, response, time):
        self.logger.info(f'\n\t{request.remote} {request.method} http://{request.host}{request.path} done in {time}s: {response.status}')
