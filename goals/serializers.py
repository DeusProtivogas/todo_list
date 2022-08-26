# import transaction as transaction

from django.db import transaction
from rest_framework import serializers
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from core.serializers import UserSerializer
from core.models import User
from rest_framework.exceptions import ValidationError


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", "is_deleted")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.OWNER
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices[1:]
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):

        # owner = validated_data.pop("user")
        owner = self.context['request'].user
        new_participants = validated_data.pop("participants", [])
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = instance.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part["user"], role=new_part["role"]
                )

            if title := validated_data.get("title"):
                instance.title = title

            instance.save()

        return instance

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"




class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user", "is_deleted")
        fields = "__all__"

    def validate_board(self, value):
        if value.is_deleted:
            raise ValidationError('Not allowed to delete category')

        if not BoardParticipant.objects.filter(
            board=value,
            role__in=[BoardParticipant.Role.OWNER, BoardParticipant.Role.WRITER],
            user=self.context['request'].user
        ).exists():
            raise ValidationError("Must be owner or writer")

        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


class GoalSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")

        # if value.user != self.context["request"].user:
        #     raise serializers.ValidationError("not the owner of the category")

        if self.instance.category.board_id != value.board_id:
            raise ValidationError('Transfer between projects not allowed')

        return value


class GoalCreateSerializer(GoalSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):

        if not BoardParticipant.objects.filter(
            board=value.board_id,
            role__in=[BoardParticipant.Role.OWNER, BoardParticipant.Role.WRITER],
            user=self.context['request'].user
        ).exists():
            raise ValidationError("Must be owner or writer")

        return value


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ("id", "created", "updated")

    def validate_goal(self, value):

        # print("HERE: ", self.context['request'].user)
        if not BoardParticipant.objects.filter(
            board=value.category.board_id,
            role__in=[BoardParticipant.Role.OWNER, BoardParticipant.Role.WRITER],
            user=self.context['request'].user
        ).exists():
            # print("HERE: ", self.context['request'].user)
            raise ValidationError("Must be owner or writer")

        # print("HERE: ", self.context['request'].user)

        return value


class CommentSerializer(CommentCreateSerializer):
    # goal = GoalSerializer(read_only=True)
    user = UserSerializer(read_only=True)#, source='goal.user')

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")


# class CommentCreateSerializer(BaseGoalCommentSerializer):
#     goal = GoalSerializer(read_only=True)
#     # user = UserSerializer(read_only=True, source='owner')
