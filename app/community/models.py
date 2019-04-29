from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# 모델은 단수로 사용
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='question', null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '질문게시판'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    def __str__(self):
        return self.title


# 모델은 단수로 사용하고, 주기능을 앞에 두어 Camel-case 로 설정
class CommentQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='question_comment', null=True)
    like = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '질문게시판 댓글'
        verbose_name_plural = f'{verbose_name} 목록'
        ordering = ['-pk']

    def __str__(self):
        return self.content
