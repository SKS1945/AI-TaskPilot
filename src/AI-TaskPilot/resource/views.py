from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from resource.models import Resource


class ResourceListAPIView(APIView):
    def get(self, request):
        resources = Resource.objects.filter(is_active=True).values(
            "id", "display_name", "email", "team"
        )
        return Response(list(resources))
