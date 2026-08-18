from rest_framework import permissions


class PublicReadAuthenticatedWriteMixin:
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]

        return [permissions.IsAdminUser()]
