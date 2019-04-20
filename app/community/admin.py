from django.contrib import admin

from .models import Question, CommentQuestion

admin.site.register(Question)

admin.site.register(CommentQuestion)
