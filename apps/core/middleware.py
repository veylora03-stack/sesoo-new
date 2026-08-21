"""Core middleware utilities."""


class AuthenticatedUserCacheBypass:
    """Bypass the site-wide page cache for authenticated users and non-idempotent methods.

    Safe to place anywhere in MIDDLEWARE: guards against a missing request.user
    (e.g. when positioned before AuthenticationMiddleware).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user is not None and getattr(user, "is_authenticated", False):
            request._cache_update_cache = False
        if request.method not in ("GET", "HEAD"):
            request._cache_update_cache = False
        return self.get_response(request)