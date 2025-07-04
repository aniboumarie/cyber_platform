from django.db import models
from django.contrib.auth.models import User # Import User model
from django.utils.text import slugify # For auto-generating slugs
from fernet_fields import EncryptedTextField

class Course(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True, help_text="URL-friendly version of the title. Leave blank to auto-generate.")
    summary = models.TextField(help_text="Short description for catalog page")
    description = models.TextField(help_text="Detailed description for course detail page")
    instructor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'groups__name': 'Trainer'},
        help_text="Trainer for this course"
    )
    key_topics = models.TextField(blank=True, null=True, help_text="List key topics, ideally one per line for simple display.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True, help_text="URL-friendly version of the title. Leave blank to auto-generate.")
    content = models.TextField(help_text="Content of the lesson (can be Markdown or HTML)")
    order = models.PositiveIntegerField(help_text="Order of the lesson within the course")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'order'] # Order by course, then by lesson order
        unique_together = [
            ('course', 'slug'), # Ensure lesson slugs are unique within a course
            ('course', 'order')  # Ensure order is unique within a course
        ]

    def __str__(self):
        return f"{self.course.title} - Lesson {self.order}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0, help_text="Percentage of course completion, e.g., 0-100")

    class Meta:
        unique_together = ('user', 'course') # A user can only be enrolled in a course once

    def __str__(self):
        return f'{self.user.username} enrolled in {self.course.title}'

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)
    answer = EncryptedTextField()

    def __str__(self):
        return self.question


# Create your models here.
