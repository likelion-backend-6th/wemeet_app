import os

from .base import *

DEBUG = False

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

LOCAL_IP = os.getenv("LOCAL_IP", "localhost")
