from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission
def extract_answers(request):
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_answers.append(choice_id)
    return submitted_answers


def submit(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=user, course=course)
    submission = Submission.objects.create(enrollment=enrollment)
    choices = extract_answers(request)
    submission.choices.set(choices)
    return HttpResponseRedirect(
        reverse(viewname='onlinecourse:show_exam_result', args=(course.id, submission.id))
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    selected_ids = list(submission.choices.values_list('id', flat=True))

    total_score = 0
    score = 0
    for lesson in course.lesson_set.all():
        for question in lesson.question_set.all():
            total_score += question.grade
            if question.is_get_score(selected_ids):
                score += question.grade

    grade = int((score / total_score) * 100) if total_score else 0

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': grade,
    }
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)
