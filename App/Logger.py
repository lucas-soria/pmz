from aiohttp.abc import AbstractAccessLogger
from concurrent import futures
from datetime import datetime


class AccessLogger(AbstractAccessLogger):

    def log(self, request, response, time):
        INFO = f'{request.method} {request.path}  RESULT:{response.status}'
        DEBUG = f'{request.remote} {request.method} {request.path} RESULT:{response.status}. Done in:{time}s'
        with futures.ThreadPoolExecutor(max_workers=1) as thread:
            thread.submit(self.log_with_threads, INFO, DEBUG)

    def log_with_threads(self, INFO, DEBUG):
        self.logger.info(INFO)
        self.logger.debug(DEBUG)
        DEBUG = datetime.today().isoformat() + ' ' + DEBUG + '\n'
        try:
            with open('./Logs/log.txt', 'a') as file:
                file.write(DEBUG)
        except FileNotFoundError:
            with open('./Logs/log.txt', 'w') as file:
                file.write(DEBUG)
