from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
from datetime import timedelta
AXES_FAILURE_LIMIT = 20
AXES_COOLOFF_TIME = timedelta(minutes=2)
