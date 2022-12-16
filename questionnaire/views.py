from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from questionnaire.forms import *
from questionnaire.models import Questionnaire, Result, Question, Answer
from questionnaire.utils import calculate_result

log = logging.getLogger(__name__)


@login_required
def questionnaires(request):
    context = dict()

    context["questionnaires"] = Questionnaire.objects.all()

    return render(request, "questionnaires.html", context)


@login_required
def questionnaire_info(request, questionnaire_id):
    context = dict()

    selected_questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    context["questionnaire"] = selected_questionnaire
    context["questions_total"] = Question.objects.filter(questionnaire=selected_questionnaire).count()

    return render(request, "questionnaire_info.html", context)


@login_required
def question_of_questionnaire(request, result_id, questionnaire_id, question_number):
    context = dict()

    questionnaire = Questionnaire.objects.get(id=questionnaire_id)
    context["questionnaire"] = questionnaire

    if question_number == 0 and result_id == 0:
        questions = Question.objects.filter(questionnaire=questionnaire).order_by('number', 'text', 'id')
        context["questions"] = questions

        result = Result(testee=request.user,
                        questionnaire=questionnaire,
                        current_question_id=questions.first().id)
        result.save()
        counter = 1
        for question in questions:
            Answer(result=result, question=question, number=counter).save()
            counter += 1

        context["answer_give_form"] = AnswerGiveForm()

        return HttpResponseRedirect(reverse('question_of_questionnaire',
                                            kwargs={'result_id': int(result.id),
                                                    'questionnaire_id': int(questionnaire_id),
                                                    'question_number': int(1)}))

    questions_total = Question.objects.filter(questionnaire=questionnaire).count()
    context["last_question"] = True if question_number == questions_total else False
    context["questions_total"] = questions_total

    result = Result.objects.get(id=result_id)
    answer = Answer.objects.filter(result=result).get(number=question_number)
    context["question"] = answer.question
    context["question_number"] = question_number

    if "action" in request.POST and request.POST['action'] in ["save_answer_and_go_next", "save_answer_and_finish"]:
        form = AnswerGiveForm(request.POST)
        if form.is_valid():
            form.save(answer=answer)
            if request.POST['action'] == "save_answer_and_go_next":
                return HttpResponseRedirect(reverse('question_of_questionnaire',
                                                    kwargs={'result_id': int(result.id),
                                                            'questionnaire_id': int(questionnaire_id),
                                                            'question_number': int(question_number + 1)}))
            if request.POST['action'] == "save_answer_and_finish":
                return HttpResponseRedirect(reverse('result_of_questionnaire',
                                                    kwargs={'result_id': int(result.id)}))
        else:
            log.error(form.errors.as_data())

    context["answer_give_form"] = AnswerGiveForm()
    return render(request, "question_of_questionnaire.html", context)


@login_required
def result_of_questionnaire(request, result_id):
    context = dict()

    result = Result.objects.get(id=result_id)
    questionnaire = Questionnaire.objects.get(result=result)
    context["questionnaire"] = questionnaire
    context["questions_total"] = Question.objects.filter(questionnaire=questionnaire).count()

    calculate_result(result)

    context["correct_answers_counter"] = result.correct_answers_counter
    context["incorrect_answers_counter"] = result.incorrect_answers_counter
    context["percent_of_correct_answers"] = 100*result.correct_answers_counter / context["questions_total"]

    context["result_id"] = result_id

    return render(request, "result_of_questionnaire.html", context)




