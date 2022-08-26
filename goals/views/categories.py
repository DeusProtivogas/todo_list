from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from goals.models import GoalCategory, Goal
from goals.serializers import GoalCategorySerializer, GoalCategoryCreateSerializer
from goals.permissions import GoalCategoryPermissions


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    # permission_classes = [IsAuthenticated]
    permission_classes = [GoalCategoryPermissions]
    # необходимо добавить serializer
    serializer_class = GoalCategoryCreateSerializer

class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_fields = ['board', "user"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )

class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.goals.update(status=Goal.status.archived)
            # Goal.objects.filter(category=instance).update(status=Goal.status.archived)
            instance.save()

        return instance

