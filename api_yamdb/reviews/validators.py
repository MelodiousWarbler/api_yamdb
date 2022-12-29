import re

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
    if re.search(r'^[\w_.@+-]+$', value) is None:
        raise ValidationError(
            ('Допустимы буквы, цифры и символы _.@+-'),
            params={'value': value},
        )
