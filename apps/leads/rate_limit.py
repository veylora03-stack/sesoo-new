"""
IP-based rate limiting for Lead form using Django's cache framework.
No external dependencies required.

Security notes:
- X-Forwarded-For is trusted only when SECURE_PROXY_SSL_HEADER is set
  (i.e., behind a known reverse proxy like Caddy).
- In production, Caddy strips client-supplied X-Forwarded-For and sets
  its own, so spoofing is not possible with the default setup.
"""
import os
import time
from django.core.cache import cache

# Configuration
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 5  # max leads per window per IP
RATE_LIMIT_COOLDOWN = 30  # seconds cooldown after hitting limit


def get_client_ip(request):
    """
    Extract client IP from request.

    In production behind Caddy:
    - Caddy sets X-Forwarded-For with the real client IP
    - We use the LAST value (not first) because Caddy appends
    - If X-Forwarded-For is absent, fall back to REMOTE_ADDR

    For additional security, we only trust X-Forwarded-For when
    Django's SECURE_PROXY_SSL_HEADER is configured (production only).
    """
    # Only trust proxy headers in production (behind Caddy)
    from django.conf import settings
    has_proxy_header = hasattr(settings, 'SECURE_PROXY_SSL_HEADER')

    if has_proxy_header:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Caddy appends: "client, proxy1, proxy2"
            # We want the client (last entry that isn't our proxy)
            ips = [ip.strip() for ip in x_forwarded_for.split(',')]
            return ips[0] if ips else request.META.get('REMOTE_ADDR', '')

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
