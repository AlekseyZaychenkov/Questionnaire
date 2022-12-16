import logging
from django.contrib import admin
from django import forms

from questionnaire.models import Question, Questionnaire, Result, Answer
from questionnaire.validators import validate_not_negative, validator_for_amount_correct_options

log = logging.getLogger(__name__)


class QuestionForm(forms.ModelForm):
    questionnaire = forms.ModelChoiceField(queryset=Questionnaire.objects.all())
    number = forms.IntegerField(required=False, validators=[validate_not_negative])
    text = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={"rows": 3, "cols": 100}))
    option_1 = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={"rows": 2, "cols": 100}))
    option_1_correct = forms.BooleanField(required=False)
    option_2 = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={"rows": 2, "cols": 100}))
    option_2_correct = forms.BooleanField(required=False)
    option_3 = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={"rows": 2, "cols": 100}), required=False)
    option_3_correct = forms.BooleanField(required=False)
    option_4 = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={"rows": 2, "cols": 100}), required=False)
    option_4_correct = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        validator_for_amount_correct_options(cleaned_data)
        return cleaned_data

    class Meta:
        model = Question
        exclude = ['id']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'number', 'get_questionnaire_title')
    form = QuestionForm

    @admin.display(ordering='questionnaire__title', description='Questionnaire')
    def get_questionnaire_title(self, obj):
        return obj.questionnaire.title


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'get_questions_text')

    @admin.display(description='Questions')
    def get_questions_text(self, questionnaire):
        questions = list(map(lambda x: "(" + str(x.number) + "): " + x.text + "\n",
                             Question.objects.filter(questionnaire=questionnaire).order_by('number')))
        return questions


class QuestionnaireInline(admin.TabularInline):
    model = Questionnaire
    raw_id_fields = ("questions",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('get_result_title', 'questionnaire', 'testee', 'correct_answers_counter',
                    'incorrect_answers_counter')

    @admin.display(ordering='testee', description='Title')
    def get_result_title(self, obj):
        return f"Result object({obj.id})"


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('get_answer_title', 'result', 'question')

    @admin.display(ordering='result', description='Title')
    def get_answer_title(self, obj):
        return f"Answer object({obj.id})"
