from .base import *
import os
import logging

logger = logging.getLogger(__name__)

DEBUG = False

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in production environment.")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS if h.strip()]
if not ALLOWED_HOSTS:
    raise ValueError("ALLOWED_HOSTS must be set in production environment.")

# --- Redis is MANDATORY in production ---
REDIS_URL = os.getenv("REDIS_URL", "")
if not REDIS_URL:
    raise ValueError(
        "REDIS_URL must be set in production. "
        "Session engine requires Redis. Example: redis://redis:6379/0"
    )

# --- PostgreSQL is MANDATORY in production ---
DB_ENGINE = os.getenv("DB_ENGINE", "")
if DB_ENGINE != "postgresql":
    raise ValueError(
        "DB_ENGINE=postgresql must be set in production. "
        "SQLite is not supported in production."
    )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "sesoo_db"),
        "USER": os.getenv("DB_USER", ""),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# --- Security ---
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "True").lower() in ("true", "1", "yes")
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --- WhiteNoise ---
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    try:
        sec_idx = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
        MIDDLEWARE.insert(sec_idx + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    except ValueError:
        MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- Logging ---
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# --- Redis Cache (mandatory, validated above) ---
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.middleware.AuthenticatedUserCacheBypass',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'sesoo'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# --- Sentry (optional) ---
sentry_dsn = os.environ.get("SENTRY_DSN")
if sentry_dsn:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        from sentry_sdk.integrations.redis import RedisIntegration

        try:
            import subprocess
            release = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode("utf-8").strip()
        except Exception:
            release = "unknown"

        sentry_sdk.init(
            dsn=sentry_dsn,
            integrations=[DjangoIntegration(), RedisIntegration()],
            traces_sample_rate=0.1,
            send_default_pii=False,
            environment="production",
            release=release,
        )
    except ImportError:
        logger.warning("sentry-sdk is not installed. Sentry monitoring disabled.")
else:
    logger.warning("SENTRY_DSN is not set. Sentry monitoring is disabled.")
