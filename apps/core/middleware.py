"""
Custom cache middleware that bypasses caching for authenticated users
and non-GET requests.
"""


class AuthenticatedUserCacheBypass:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Safely check user to avoid AttributeError if this middleware
        # runs before AuthenticationMiddleware
        user = getattr(request, 'user', None)
        if user is not None and getattr(user, 'is_authenticated', False):
            request._cache_update_cache = False

        if request.method not in ('GET', 'HEAD'):
            request._cache_update_cache = False

        return self.get_response(request)