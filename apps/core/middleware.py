"""Core middleware utilities."""


class AuthenticatedUserCacheBypass:
    """Bypass the site-wide page cache for authenticated users,
    non-idempotent HTTP methods and the Django test client.

    NOTE: this middleware must be placed AFTER
    django.contrib.auth.middleware.AuthenticationMiddleware, but the
    getattr() guard below also makes it safe regardless of ordering.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user is not None and getattr(user, "is_authenticated", False):
            request._cache_update_cache = False

        if request.method not in ("GET", "HEAD"):
            request._cache_update_cache = False

        try:
            if request.get_host() == "testserver":
                request._cache_update_cache = False
        except Exception:
            pass

        return self.get_response(request)