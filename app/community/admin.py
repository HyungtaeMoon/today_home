from django.contrib import admin

from .models import Question, CommentQuestion


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'content']


@admin.register(CommentQuestion)
class CommentQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'content']
