"""
Test-specific settings that override production settings
to make tests work without collectstatic and SSL.
"""
from config.settings.base import *

# Use default storage for tests (no hashing)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Disable SSL redirect for tests
SECURE_SSL_REDIRECT = False

# Use locmem cache for tests (avoid Redis dependency)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Use database sessions for tests (avoid cache dependency)
SESSION_ENGINE = "django.contrib.sessions.backends.db"
