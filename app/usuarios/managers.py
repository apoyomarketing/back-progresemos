from django.contrib.auth.base_user import BaseUserManager


class UsuarioManager(BaseUserManager):

    def create_user(self, email, nombre, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio")

        email = self.normalize_email(email)

        usuario = self.model(
            email=email,
            nombre=nombre,
            **extra_fields
        )

        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, email, nombre, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("estado", True)

        return self.create_user(
            email=email,
            nombre=nombre,
            password=password,
            **extra_fields
        )