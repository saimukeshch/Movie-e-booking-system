from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator, ASCIIUsernameValidator
from django.core import validators
from django.utils.translation import gettext as _

class UserManager(BaseUserManager):
    def create_user(self, user_name, email, password=None, **extra_fields):
        if not user_name:
            raise ValueError('The username field must be set')
        user_name = self.normalize_email(user_name)
        user = self.model(user_name=user_name, email = email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(user_name = user_name, email = email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator() if hasattr(validators, 'UnicodeUsernameValidator') else ASCIIUsernameValidator()

    user_name = models.CharField(unique=True, max_length=50, validators=[username_validator])
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(_('password'), max_length=128,
        validators=[validators.MinLengthValidator(8), validators.RegexValidator(
            regex='^(?=.*[A-Z])(?=.*\d).*$', message=_("Your password must contain at least 8 characters, including one uppercase letter and one digit."), code='invalid_password'
        )]
    )
    address = models.CharField(max_length=200)
    phone = models.IntegerField(default = None,null=True,blank=True)
    enrollForPromotions = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email','password','is_admin','is_staff','is_active']

    objects = UserManager()

    def __str__(self):
        return self.user_name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
    
    def has_perm(self, perm, obj=None):
        if self.is_admin and self.is_staff and self.is_active:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_admin and self.is_staff and self.is_active:
            return True
        return False
