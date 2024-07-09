from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator,
)


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def __init__(self, user_attributes=('username', 'email'), max_similarity=0.8):
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

        def validate(self, password, user=None):
            if user in None:
                return
            for attribute_name in self.user_attributes:
                value = getattr(user, attribute_name, None)
                if not value or not isinstance(value, str):
                    continue

                try:
                    super().validate(password, user)
                except ValidationError:
                    raise ValidationError(
                        _("Twoje hasło jest zbyt podobne do twoich innych danych osobowych."),
                        code='password_too_similar'
                    )


class CustomMinimumLenghtValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError:
            raise ValidationError(
                _("Twoje hasło jest zbyt krótkie. Powinno zawierać  co najmniej %(min_length)s znaków"),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Twoje hasło musi zawierać co najmniej %(min_length)d znaków."
        ) % {'min_length': self.min_length}


class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user):
        try:
            super().validate(password, user=None)
        except ValidationError:
            raise ValidationError(
                _("Twoje hasło jest zbyt popularne. Proszę użyć trudniejszego hasła."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("Twoje hasło jest zbyt powszechnie używane.")


class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user):
        try:
            super().validate(password, user)
        except ValidationError:
            raise ValidationError(
                _("Hasło nie może być w całości numeryczne."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Twoje hasło nie może w całości składać się z cyfr.")
