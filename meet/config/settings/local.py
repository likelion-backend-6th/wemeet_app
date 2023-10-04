import os

from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "*",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8888",
]
