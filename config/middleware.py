from django.http import HttpResponsePermanentRedirect
from django.urls import Resolver404
from django.urls import resolve


class TrailingSlashMiddleware:
    """
    Middleware to remove trailing slashes from URLs, while ignoring certain routes.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = ["/admin/", "/cms/", "/api/"]

    def __call__(self, request):
        path = request.path
        if any(path.startswith(excluded) for excluded in self.excluded_paths):
            return self.get_response(request)

        if path != "/" and path.endswith("/"):
            try:
                resolve(path.rstrip("/"))
                return HttpResponsePermanentRedirect(path.rstrip("/"))
            except Resolver404:
                pass

        return self.get_response(request)
