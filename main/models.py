from django.db import models
from fernet_fields import EncryptedTextField

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = EncryptedTextField()

    def __str__(self):
        return self.question


# Create your models here.
