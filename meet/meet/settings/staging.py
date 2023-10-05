import os

from .base import *

DEBUG = True

LOCAL_IP = os.getenv("LOCAL_IP", "localhost")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "*",
    LOCAL_IP,
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8888",
]
