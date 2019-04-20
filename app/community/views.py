from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .models import Question, CommentQuestion
from .forms import QuestionCreateForm, CommentCreateForm


User = get_user_model()


def questions(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'community/questions.html', context)


def question_detail(request, question_pk):
    question_detail = Question.objects.get(pk=question_pk)
    comment_list = CommentQuestion.objects.filter(question_id=question_detail.pk)
    context = {
        'question_detail': question_detail,
        'comment_list': comment_list,
    }
    return render(request, 'community/question_detail.html', context)


@login_required
def question_create(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        # form 을 받을 때 request.POST, request.FILES 순서대로 정의해야 함
        # form.is_valid() 상태여도 데이터가 unbound 상태
        form = QuestionCreateForm(request.POST, request.FILES)
        if user is not None:
            if form.is_valid():
                question = form.save(commit=False)
                question.user = request.user
                question.title = form.cleaned_data['title']
                question.content = form.cleaned_data['content']
                question.image = form.cleaned_data['image']
                form.save()
                return redirect('community:questions')
    else:
        form = QuestionCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'community/question-create.html', context)


class QuestionDeleteView(DeleteView):
    """질문 게시판 글 삭제"""
    model = Question

    success_url = reverse_lazy('community:questions')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.user == self.request.user:
            return redirect('community:questions')
        return redirect('community:questions')


# 질문게시판 1개를 삭제하기 때문에 단수 question
question_delete = QuestionDeleteView.as_view()


# def comment_create(request, community_pk):
#     if request.method == 'POST':
#         community = Community.objects.get(pk=community_pk)
#         form = CommentCreateForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.community = community
#             comment.author = request.user
#             comment.save()
#             return redirect('community:detail')
#
#     else:
#         form = CommentCreateForm()
#         context = {
#             'form': form,
#         }
#         return render(request, 'community/community_detail.html', context)

@login_required
def comment_create(request, question_pk):
    if request.method == 'POST':
        question = Question.objects.get(pk=question_pk)

        form = CommentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.question = question
            comment.content = form.cleaned_data['content']
            comment.image = form.cleaned_data['image']
            form.save()
            return redirect('community:question-detail', question.pk)

    form = CommentCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'community/comment-create.html', context)
