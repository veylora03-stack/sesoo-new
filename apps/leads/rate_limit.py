"""
IP-based rate limiting for Lead form using Django's cache framework.
No external dependencies required.
"""
import time
from django.core.cache import cache

# Configuration
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 5  # max leads per window per IP
RATE_LIMIT_COOLDOWN = 30  # seconds cooldown after hitting limit


def get_client_ip(request):
    """Extract client IP from request, respecting X-Forwarded-For behind reverse proxy."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def is_rate_limited(request):
    """
    Check if request is rate limited.
    Returns (is_limited: bool, remaining: int, retry_after: int).
    """
    ip = get_client_ip(request)
    if not ip:
        return False, RATE_LIMIT_MAX_REQUESTS, 0

    cache_key = f"lead_rate:{ip}"
    cooldown_key = f"lead_cooldown:{ip}"

    # Check cooldown
    cooldown_until = cache.get(cooldown_key)
    if cooldown_until:
        retry_after = int(cooldown_until - time.time())
        if retry_after > 0:
            return True, 0, retry_after
        else:
            cache.delete(cooldown_key)

    # Get current count
    data = cache.get(cache_key)
    if data is None:
        data = {"count": 0, "window_start": time.time()}

    # Reset window if expired
    elapsed = time.time() - data["window_start"]
    if elapsed > RATE_LIMIT_WINDOW:
        data = {"count": 0, "window_start": time.time()}

    # Check limit
    if data["count"] >= RATE_LIMIT_MAX_REQUESTS:
        cooldown_until = time.time() + RATE_LIMIT_COOLDOWN
        cache.set(cooldown_key, cooldown_until, RATE_LIMIT_COOLDOWN)
        return True, 0, RATE_LIMIT_COOLDOWN

    return False, RATE_LIMIT_MAX_REQUESTS - data["count"], 0


def record_lead_submission(request):
    """Record a lead submission for rate limiting."""
    ip = get_client_ip(request)
    if not ip:
        return

    cache_key = f"lead_rate:{ip}"
    data = cache.get(cache_key)
    if data is None:
        data = {"count": 0, "window_start": time.time()}

    elapsed = time.time() - data["window_start"]
    if elapsed > RATE_LIMIT_WINDOW:
        data = {"count": 0, "window_start": time.time()}

    data["count"] += 1
    remaining_ttl = int(RATE_LIMIT_WINDOW - (time.time() - data["window_start"]))
    cache.set(cache_key, data, max(remaining_ttl, 1))
