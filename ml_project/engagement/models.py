from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class TextbookSection(models.Model):
    section_title = models.CharField(max_length=200)
    def __str__(self):
        return self.section_title

class TextbookPage(models.Model):
    page_title = models.CharField(max_length=200)
    sections = models.ManyToManyField(TextbookSection, related_name='pages')
    def __str__(self):
        return self.page_title

class TextbookSlide(models.Model):
    slide_title = models.CharField(max_length=200, default='')
    pages = models.ManyToManyField(TextbookPage, related_name='slides')
    def __str__(self):
        return self.slide_title

class RevisionQuestion(models.Model):
    textbook_page = models.ForeignKey(TextbookPage, on_delete=models.CASCADE, related_name='rq_questions')

class RevisionQuestionAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revision_attempts')
    question = models.ForeignKey(RevisionQuestion, on_delete=models.CASCADE, related_name='attempts')
    viewed = models.DateTimeField(null=True, blank=True)
    correct = models.DateTimeField(null=True, blank=True)
    processed = models.BooleanField(default=False)
    def __str__(self):
        return f"Attempt by {self.user.username} on Question {self.question_id}"

class RevisionQuestionAttemptDetail(models.Model):
    attempt = models.ForeignKey(RevisionQuestionAttempt, on_delete=models.CASCADE, related_name='details')
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(default=now)
    processed = models.BooleanField(default=False)
    def __str__(self):
        return f"{'Correct' if self.is_correct else 'Incorrect'} at {self.timestamp}"

class WritingInteraction(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    page_id = models.IntegerField()
    user_input = models.TextField()
    openai_response = models.TextField()
    grade = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Interaction - Page {self.page_id}"

class UserSlideRead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slide = models.ForeignKey(TextbookSlide, on_delete=models.CASCADE)
    slide_status = models.CharField(
        max_length=10,
        choices=[('read','Read'),('unread','Unread'),('revise','Revise')],
        default='unread'
    )
    class Meta:
        unique_together = ('user','slide')
    def __str__(self):
        return f"{self.user.username} - {self.slide.slide_title} - {self.slide_status}"

class UserSlideReadSession(models.Model):
    slide_read = models.ForeignKey('UserSlideRead', on_delete=models.CASCADE, related_name='review_sessions')
    expanded = models.DateTimeField(default=now)
    collapsed = models.DateTimeField(null=True, blank=True)
    read = models.DateTimeField(null=True, blank=True)
    def read_duration(self):
        if self.expanded:
            end = self.read or self.collapsed
            if end:
                secs = int((end - self.expanded).total_seconds())
                return max(secs, 0)
        return 0
