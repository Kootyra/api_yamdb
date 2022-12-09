from rest_framework import permissions


class IsModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.role == 'moderator'


class IsAuthorModerAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return request.user.is_authenticated

        if request.method in ['PATCH', 'DELETE']:
            return (
                obj.author == request.user
                or request.user.is_superuser
                or request.user.role in ('moderator', 'admin')
            )

        return request.method in permissions.SAFE_METHODS


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff:
            return True

        return bool(hasattr(request.user, 'role')
                    and request.user.role == 'admin')
