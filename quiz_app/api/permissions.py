from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        """
        Allows GET, PATCH and DELETE methods.
        """
        if request.method in SAFE_METHODS:
            return True
        if request.method == "PATCH":
            return True
        if request.method == "DELETE":
            return True
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Only allows GET, PATCH and DELETE methods, if the provided used
        is also the owner of the quiz.
        """
        if request.method == "GET":
            return obj.user == request.user
        if request.method == "PATCH":
            return obj.user == request.user
        if request.method == "DELETE":
            return obj.user == request.user
        return False