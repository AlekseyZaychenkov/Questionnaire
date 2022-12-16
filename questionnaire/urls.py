from django.urls import path

from questionnaire.views import questionnaires, questionnaire_info, question_of_questionnaire, result_of_questionnaire


urlpatterns = [
    path('questionnaires', questionnaires, name="questionnaires"),
    path('questionnaire/questionnaire_id=<int:questionnaire_id>', questionnaire_info, name="questionnaire_info"),
    path('result/result_id=<int:result_id>/questionnaire/questionnaire_id=<int:questionnaire_id>/question_number/question_number=<int:question_number>',
         question_of_questionnaire, name="question_of_questionnaire"),
    path('result/result_id=<int:result_id>',
         result_of_questionnaire, name="result_of_questionnaire"),
]
