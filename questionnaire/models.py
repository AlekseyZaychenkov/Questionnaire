from django.db import models

from account.models import Account


class Questionnaire(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048, null=True, blank=True)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    text = models.CharField(max_length=2048, null=True, blank=True)

    option_1 = models.CharField(max_length=2048, null=True, blank=True)
    option_1_correct = models.BooleanField(default=False)
    option_2 = models.CharField(max_length=2048, null=True, blank=True)
    option_2_correct = models.BooleanField(default=False)
    option_3 = models.CharField(max_length=2048, null=True, blank=True)
    option_3_correct = models.BooleanField(default=False)
    option_4 = models.CharField(max_length=2048, null=True, blank=True)
    option_4_correct = models.BooleanField(default=False)


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    testee = models.ForeignKey(Account, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    current_question_id = models.IntegerField()
    correct_answers_counter = models.IntegerField(null=True)
    incorrect_answers_counter = models.IntegerField(null=True)


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.IntegerField()

    option_1_chosen = models.BooleanField(default=False)
    option_2_chosen = models.BooleanField(default=False)
    option_3_chosen = models.BooleanField(default=False)
    option_4_chosen = models.BooleanField(default=False)
