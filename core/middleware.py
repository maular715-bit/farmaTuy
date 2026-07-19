class AuthorizationHeaderMiddleware:
    """Ensure Authorization header is available in request.META and normalized.

    Some servers/proxies may forward the header differently; this middleware
    copies common variants so code reading `request.headers['Authorization']`
    will find it.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If HTTP_AUTHORIZATION present but headers() mapping doesn't expose it,
        # make sure it's present as HTTP_AUTHORIZATION (Django request.headers uses META)
        try:
            meta_auth = request.META.get('HTTP_AUTHORIZATION') or request.META.get('Authorization')
            if meta_auth and not request.META.get('HTTP_AUTHORIZATION'):
                request.META['HTTP_AUTHORIZATION'] = meta_auth
        except Exception:
            pass
        return self.get_response(request)
