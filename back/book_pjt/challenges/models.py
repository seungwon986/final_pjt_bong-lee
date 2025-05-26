from django.db import models
from django.conf import settings
from books.models import Book


class Challenge(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_challenges')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    target_books = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='challenges', null=True, blank=True)

    def __str__(self):
        return self.title


class ChallengeParticipant(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    class Meta:
        unique_together = ('challenge', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.challenge.title}"


class ChallengeComment(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.challenge.title}"


class BookQuiz(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    choices = models.JSONField()  # {'A': '...', 'B': '...', 'C': '...', 'D': '...'}
    answer = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.question[:30]}"


class QuizAttempt(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({self.score})"
