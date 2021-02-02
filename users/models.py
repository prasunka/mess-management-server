from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, name, typeAccount, password, is_staff=False, is_superuser=False, is_active=True, specialRole=None):
        user = self.model(email=email, name=name, typeAccount=typeAccount, specialRole=specialRole)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, typeAccount, password, is_staff=True, is_superuser=True, is_active=True, specialRole=None,):
        user = self.model(email=email, name=name, typeAccount=typeAccount, specialRole=specialRole)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = is_active
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email_):
        print(email_)
        return self.get(email=email_)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    typeAccount = models.CharField(max_length=20)
    specialRole = models.CharField(max_length=100, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['name', 'typeAccount']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def natural_key(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    def __str__(self):
        return self.email
