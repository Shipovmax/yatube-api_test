from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Group, Post
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class ListCreateViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    pass


class PostViewSet(viewsets.ModelViewSet):
    """
    Просмотр постов доступен всем пользователям.
    Внесение изменений доступно только авторизированным пользователям.
    Изменение поста доступно только для автора поста.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Зарегистрированный пользователь указывается как автор поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Просмотр групп доступен всем пользователям.
    Внесение изменений доступно только авторизированным пользователям.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class CommentViewSet(viewsets.ModelViewSet):
    """
    Просмотр комментариев всем пользователям.
    Внесение изменений доступно только авторизированным пользователям.
    Изменение комментария доступно только для автора комментария.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        IsOwnerOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly
    )

    def perform_create(self, serializer):
        """Зарегистрированный пользователь указывается как автор коммента."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        """Изменение queryset для отображения данных конкретного поста."""
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments


class FollowViewSet(ListCreateViewSet):
    """
    Просмотр и изменение подписок на пользователей.
    Доступно только для авторизированных пользователей (глобальные настройки).
    """
    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("=following__username",)

    def get_queryset(self):
        """Изменение queryset для отображения данных по пользователю."""
        return self.request.user.follower.all()
