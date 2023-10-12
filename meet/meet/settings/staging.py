import os

from .base import *

DEBUG = True

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

LOCAL_IP = os.getenv("LOCAL_IP", "localhost")
