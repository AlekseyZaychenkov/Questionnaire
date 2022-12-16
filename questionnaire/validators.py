import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from questionnaire.models import Question


def validate_not_negative(value):
    if value < 1:
        raise ValidationError(
            _('%(value)s should be a positive number!'),
            params={'value': value},
        )


def validator_for_amount_correct_options(cleaned_data):
    if not (cleaned_data.get("option_1_correct") or cleaned_data.get("option_2_correct") or
            cleaned_data.get("option_3_correct") or cleaned_data.get("option_4_correct")):
        raise ValidationError("Question should have at least one correct option!")

    if (cleaned_data.get("option_1_correct") and cleaned_data.get("option_2_correct") and
            cleaned_data.get("option_3_correct") and cleaned_data.get("option_4_correct")):
        raise ValidationError("All options can not be correct!")


def validator_for_amount_correct_answers(cleaned_data):
    if not (cleaned_data.get("option_1_chosen") or cleaned_data.get("option_2_chosen") or
            cleaned_data.get("option_3_chosen") or cleaned_data.get("option_4_chosen")):
        raise ValidationError("Question should have at least one answer!")
