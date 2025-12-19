from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from skill.models import Skill


class SkillListAPIView(APIView):
    def get(self, request):
        skills = Skill.objects.all().values("id", "name", "category")
        return Response(list(skills))
