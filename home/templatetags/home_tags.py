from django import template
import math
from django.template import Library

from ..models import CardEncr

register = template.Library()

@register.simple_tag
def decrypt(s):
    fernet = CardEncr.fernet
    bites = bytes(s, 'utf-8')
    decoded = fernet.decrypt(bites).decode()
    return decoded[-4:]

register.filter('decrypt',decrypt)

@register.filter
def square(value):
    """Returns the square of the given number."""
    return value ** 2

@register.filter
def cube(value):
    """Returns the cube of the given number."""
    return value ** 3

@register.filter
def ceil(value):
    """Returns the ceiling of the given number."""
    return math.ceil(value)
