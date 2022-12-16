from questionnaire.models import Answer


def calculate_result(result):
    correct_answers_counter = 0
    incorrect_answers_counter = 0
    answers = Answer.objects.filter(result=result)

    for answer in answers:
        question = answer.question

        if question.option_1_correct != answer.option_1_chosen:
            incorrect_answers_counter += 1
            continue
        if question.option_2_correct != answer.option_2_chosen:
            incorrect_answers_counter += 1
            continue

        if question.option_3:
            if question.option_3_correct != answer.option_3_chosen:
                incorrect_answers_counter += 1
                continue
        if question.option_1:
            if question.option_1_correct != answer.option_1_chosen:
                incorrect_answers_counter += 1
                continue

        correct_answers_counter += 1

    result.correct_answers_counter = correct_answers_counter
    result.incorrect_answers_counter = incorrect_answers_counter
    result.save()