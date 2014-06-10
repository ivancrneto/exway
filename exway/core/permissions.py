""" Module for controlling API permissions """

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ Custom permissions to only allow a user read, update, create or delete
        its own expenses """

    def has_object_permission(self, request, view, obj):
        """ Only allow if the owner of the object is the same user performing
            the request """
        if not obj:
            return True
        return obj.user == request.user
