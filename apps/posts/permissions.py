from rest_framework import permissions


# permission to identify if a user is the owner of the post
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author