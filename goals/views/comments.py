from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from goals.models import GoalComment

from goals.serializers import CommentCreateSerializer, CommentSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated



class CommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = CommentCreateSerializer

    permission_classes = [IsAuthenticated]


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.all() #filter(goal__user=self.request.user)



class CommentListView(ListAPIView):
    model = GoalComment
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
    ]

    filterset_fields = ['goal']
    ordering = "-id"

    def get_queryset(self):
        return GoalComment.objects.all() #filter(goal__user=self.request.user)


