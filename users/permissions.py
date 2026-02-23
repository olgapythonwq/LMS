from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsModerator(permissions.BasePermission):
    """Проверяет, является ли пользователь Модератором."""

    def has_permission(self, request, view):
        # проверяет, входит ли пользователь в группу Moderators
        return request.user.groups.filter(name="Moderators").exists()


class IsNotModerator(BasePermission):
    """Проверяет, не является ли пользователь Модератором."""

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Moderators').exists():  # если пользователь в группе moderator — запрет
            return False
        return True


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем объекта."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsSelf(BasePermission):
    """Разрешает доступ только к своему профилю пользователя."""

    def has_object_permission(self, request, view, obj):
        return obj == request.user
