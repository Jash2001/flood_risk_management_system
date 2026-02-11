from rest_framework.permissions import BasePermission

class IsCommandCenter(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'userprofile') and \
               request.user.userprofile.role == 'COMMAND_CENTER'


class IsFieldResponder(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'userprofile') and \
               request.user.userprofile.role == 'FIELD_RESPONDER'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or (
            hasattr(request.user, 'userprofile') and
            request.user.userprofile.role == 'ADMIN'
        )
