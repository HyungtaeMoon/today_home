from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView

from .models import Question, CommentQuestion
from .forms import QuestionCreateForm, CommentCreateForm


User = get_user_model()


class QuestionListView(ListView):
    """
    model 또는 queryset 으로 원하는 데이터를 불러옴
    model -> <class 'community.models.Question>
    queryset -> <QuerySet [<Question: 궁금한게 있어요>...]>
    """
    template_name = 'question_list.html'
    queryset = Question.objects.all()
    # model = Question
    context_object_name = 'question_list'
    paginate_by = 5


questions = QuestionListView.as_view()


class QuestionDetailView(DetailView):
    """
    model, queryset, get_object() 중에서 하나만 선택하여 DB 에 접근해도 정상 작동함
    """
    template_name = 'community/question_detail.html'
    # model = Question
    # queryset = Question.objects.all()

    def get_object(self):
        return get_object_or_404(Question, pk=self.kwargs.get('pk', None))


question_detail = QuestionDetailView.as_view()

# def question_detail(request, question_pk):
#     """
#     question <- commentquestion 이 FK 로 참조하고 있는데 이를 활용하지 않고 comment_list 를 컨텍스트에 따로 받다니..
#     question.commentquestion_set.all 로 컨텍스트에 뿌리면 되는데 너무 무식했다.
#     """
#     question_detail = Question.objects.get(pk=question_pk)
#     comment_list = CommentQuestion.objects.filter(question__id=question_detail.pk)
#     context = {
#         'question_detail': question_detail,
#         'comment_list': comment_list,
#     }
#     return render(request, 'community/question_detail.html', context)


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

# @login_required
# def question_create(request):
#     user = request.user
#     if request.method == 'POST':
#         form = QuestionCreateForm(request.POST)
#         file_form = FileModelForm(request.POST, request.FILES)
#         files = request.FILES.getlist('image')
#         if form.is_valid() and file_form.is_valid():
#             question_instance = form.save(commit=False)
#             question_instance.user = user
#             question_instance.save()
#             for f in files:
#                 file_instance = QuestionFile(file=f, question=question_instance)
#                 file_instance.save()
#                 return redirect('community:questions')
#     else:
#         form = QuestionCreateForm()
#         file_form = QuestionFile()
#         context = {
#             'form': form,
#             'file_form': file_form,
#         }
#
#         return render(request, 'community/question-create.html', context)


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
            # comment.user = request.user
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
