from django.core.exceptions import ValidationError


def validate_email(value):
    email = value
    if ".edu" in email:
        raise ValidationError("We do not accept edu emails")


CATEGORIES = ['Mexican', 'Asian', 'American', 'Whatever']


def validate_category(value):
    cat = value.capitalize()
    if value not in CATEGORIES and cat not in CATEGORIES:
        raise ValidationError(f"{value} is not a valid category")
