from rest_framework.permissions import BasePermission, SAFE_METHODS
from quiz_app.models import Quiz

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "PATCH":
            return True
        if request.method == "DELETE":
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return obj.user == request.user
        if request.method == "PATCH":
            return obj.user == request.user
        if request.method == "DELETE":
            return obj.user == request.user
        return False