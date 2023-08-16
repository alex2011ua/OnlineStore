from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return request.user.role == "A"


class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return request.user.role in "MA"


class AuthUserPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return request.user.role in "UMA"


class GuestUserPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user.role)
        return request.user.role in "GUMA"
