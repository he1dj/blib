from django.http import HttpResponsePermanentRedirect
from django.urls import Resolver404
from django.urls import resolve


class TrailingSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path != "/" and path.endswith("/"):
            try:
                resolve(path.rstrip("/"))
                return HttpResponsePermanentRedirect(path.rstrip("/"))
            except Resolver404:
                pass
        return self.get_response(request)
