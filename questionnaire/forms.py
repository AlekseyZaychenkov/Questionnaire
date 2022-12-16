from django import forms
from questionnaire.validators import validator_for_amount_correct_answers
import logging

log = logging.getLogger(__name__)


class ChosenOptionForm(forms.Form):
    question = forms.CharField()


class AnswerGiveForm(forms.Form):
    option_1_chosen = forms.BooleanField(required=False)
    option_2_chosen = forms.BooleanField(required=False)
    option_3_chosen = forms.BooleanField(required=False)
    option_4_chosen = forms.BooleanField(required=False)

    def save(self, answer, commit=True):
        answer.option_1_chosen = self.cleaned_data["option_1_chosen"]
        answer.option_2_chosen = self.cleaned_data["option_2_chosen"]
        answer.option_3_chosen = self.cleaned_data["option_3_chosen"]
        answer.option_4_chosen = self.cleaned_data["option_4_chosen"]

        if commit:
            answer.save()

    def clean(self):
        cleaned_data = super().clean()
        validator_for_amount_correct_answers(cleaned_data)
        return cleaned_data
