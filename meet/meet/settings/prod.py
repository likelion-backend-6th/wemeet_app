import os

from .base import *

DEBUG = False

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

LOCAL_IP = os.getenv("LOCAL_IP", "localhost")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "*",
    LOCAL_IP,
]
