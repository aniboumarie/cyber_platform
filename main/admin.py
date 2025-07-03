from django.contrib import admin
from .models import Course, Lesson, Enrollment, Quiz # Added Quiz for completeness

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'instructor__username')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('instructor', 'created_at')

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'updated_at')
    search_fields = ('title', 'content', 'course__title')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('course',)
    ordering = ('course', 'order')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at', 'progress')
    search_fields = ('user__username', 'course__title')
    list_filter = ('course', 'enrolled_at')
    autocomplete_fields = ['user', 'course'] # For easier selection if many users/courses

class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'lesson')
    search_fields = ('question', 'lesson__title')
    list_filter = ('lesson__course',) # Filter by course via lesson
    autocomplete_fields = ['lesson']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Quiz, QuizAdmin) # Registering existing Quiz model too
