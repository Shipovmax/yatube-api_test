from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем (кто прошел проверку на аутентификацию)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Изменение/удаление только для автора
        return obj.author == request.user