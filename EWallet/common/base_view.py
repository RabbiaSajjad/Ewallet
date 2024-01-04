from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import LimitOffsetPagination
from django.contrib.auth.mixins import LoginRequiredMixin
from inflect import engine
import re as regex
from django.apps import apps

class BaseView(APIView, LimitOffsetPagination):
    def _save_resource(self, resource, request, success_status=status.HTTP_200_OK):
        if resource.is_valid():
            resource.save()
            return Response({engine().plural(self._model_name): resource.data, "message": "Resource saved successfully"}, status=success_status)
        return HttpResponse("Unprocessable entity")

    def _find_resource(self, id):
        try:
            return self._model.objects.get(id=id)
        except ObjectDoesNotExist:
            pass

    @property
    def _model(self):
        return apps.get_model('user', self._model_class_name, require_ready=True)

    @property
    def _model_class_name(self):
        return type(self).__name__.replace('View', '')

    @property
    def _model_name(self):
        name = regex.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', self._model_class_name)
        return regex.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()
