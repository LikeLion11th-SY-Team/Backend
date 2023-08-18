from django.db import models
from users.models import User

class LearningProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learning_progress')
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Learning Progress: {self.progress}"
