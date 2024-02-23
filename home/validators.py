from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from users.models import User

def validate_password(value):
    # Check if the password is at least 8 characters long
    if len(value) < 8:
        raise ValidationError(
            _("The password must be at least 8 characters long."),
            code='password_too_short',
        )
    # Check if the password contains at least one uppercase letter
    if not any(char.isupper() for char in value):
        raise ValidationError(
            _("The password must contain at least one uppercase letter."),
            code='password_no_uppercase',
        )
    # Check if the password contains at least one digit
    if not any(char.isdigit() for char in value):
        raise ValidationError(
            _("The password must contain at least one digit."),
            code='password_no_digit',
        )

def confirm_password(password,password1):
    if(password != password1):
        raise ValidationError(
            _("The passwords entered do not match. Please try again."),
            code="passwords do not match",
        )

def validate_email(email):
    if User.objects.filter(email=email).exists():
            raise ValidationError(
             _("Email already exists in the system.Login to continue."),
            code='email_already_exists',
        )

def validate_username(user_name):
    if User.objects.filter(user_name=user_name).exists():
            raise ValidationError(
             _("Username already exists in the system. Choose another username."),
            code='username_already_exists',
        )