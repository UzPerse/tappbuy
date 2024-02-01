from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, phone_number):
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,

        )

        user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self):
        pass
