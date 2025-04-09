from rest_framework import permissions


class SingleObjPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            if request.user == obj.clientId:
                return True
            elif request.user.role.name == 'ADMIN':
                return True
            return False
        if request.user == obj.clientId:
            return True
        return False
