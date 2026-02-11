from rest_framework.permissions import BasePermission, SAFE_METHODS

class IncidentPermission(BasePermission):
    def has_permission(self, request, view):
        role = getattr(request.user.userprofile, 'role', None)

        if request.method in SAFE_METHODS:
            return role in ['COMMAND_CENTER', 'ADMIN', 'NGO', 'FIELD_RESPONDER']

        return role in ['FIELD_RESPONDER', 'NGO']

class CommandCenterPermission(BasePermission):
    def has_permission(self, request, view):
        role = getattr(request.user.userprofile, 'role', None)
        return role == 'COMMAND_CENTER'
