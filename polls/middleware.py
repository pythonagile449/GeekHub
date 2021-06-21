import time
import json
from threading import local
import logging
from django.http import HttpResponse
logger = logging.getLogger(__name__)


class RequestTimeMiddleware():
    def __init__(self, get_response, *args, **kwargs):
        self.get_response = get_response

    def __call__(self, request):
        timestamp = time.monotonic()
        response = self.get_response(request)
        data = {
            'path': request.path,
            'request_total': round(time.monotonic() - timestamp, 3),
            'debug': self.log_debug,

        }
        with open('polls/debug.log', 'a') as f:
            f.write(json.dumps(data) + '\n')


        return response