class Question(models.Model):
    # Foreign key to the course (required by the grader)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    # Kept so QuestionInline still works inside LessonAdmin (Task 2)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return "Question: " + self.question_text

    def save(self, *args, **kwargs):
        # If a question is added from a lesson, fill in its course automatically
        if self.lesson_id and not self.course_id:
            self.course = self.lesson.course
        super().save(*args, **kwargs)

    # returns True if the learner selected exactly the correct choices
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        selected_total = self.choice_set.filter(id__in=selected_ids).count()
        return all_answers == selected_correct == selected_total


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return "Submission " + str(self.id) + " by " + self.enrollment.user.username
