from typing import Any, Dict  # python 3.7

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)
    group = SlugRelatedField(
        slug_field="pk", queryset=Group.objects.all(), required=False
    )

    class Meta:
        fields = ("id", "author", "text", "pub_date", "image", "group")
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", "title", "slug", "description")
        model = Group


class CommentSerializer(serializers.ModelSerializer):
    """
    Обращение ко всем комментарием поста posts/<int:post_pk>/comments.
    Обращение к комментарию posts/<int:post_pk>/comments/<int:comment_pk>.
    """

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    post = serializers.SlugRelatedField(read_only=True, slug_field="pk")

    class Meta:
        fields = ("id", "author", "post", "text", "created")
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field="username",
        queryset=User.objects.all(),
        required=False,
    )
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("user", "following"),
                message="Вы уже подписаны на этого человека.",
            ),
        ]

        fields = ("id", "user", "following")

    def validate(self, attrs: Dict[str, Any]):
        if self.context['request'].user == attrs['following']:
            raise serializers.ValidationError(
                'Подписка на самого себя запрещена.')
        return attrs
