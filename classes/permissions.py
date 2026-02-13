from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrStaffOrReadonly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated and request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return (request.user.is_authenticated and request.user.is_superuser)

# class IsAdminOrAuthor(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#         return (request.user.is)

class CustomPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            if request.user == (obj.user or request.user.is_superuser):
                return True
        if request.method in ['PATCH', 'PUT', 'CREATE', "POST"]:
            if request.user == request.user.is_staff:
                return True

class FeedBackPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
       if request.method in SAFE_METHODS:
           return True
       if request.method == 'DELETE':
           if request.user == (obj.user or request.user.is_staff):
               return True
