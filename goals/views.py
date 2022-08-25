from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalCategory
from goals.serializers import GoalCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    # необходимо добавить serializer
    serializer_class = GoalCreateSerializer
