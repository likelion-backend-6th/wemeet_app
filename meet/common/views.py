from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


def healthcheck(request):
    return JsonResponse({"status": "ok"})


def get_version(request):
    return JsonResponse({"version": settings.VERSION})


class Me(APIView):
    def get(self, request: Request):
        return Response({"pk": request.user.pk})
