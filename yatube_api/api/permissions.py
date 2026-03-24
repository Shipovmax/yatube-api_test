from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Кастомное переопределение доступа только для владельцев объекта."""

    def has_object_permission(self, request, view, obj):
        """
        GET, HEAD и OPTIONS доступны для всех запросов.
        Остальные методы только для владельцев контента.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
