from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView

from .models import Question, CommentQuestion
from .forms import QuestionCreateForm, QuestionUpdateForm, CommentCreateForm


User = get_user_model()


class QuestionListView(ListView):
    """
    model 또는 queryset 으로 원하는 데이터를 불러옴
    model -> <class 'community.models.Question>
    queryset -> <QuerySet [<Question: 궁금한게 있어요>...]>
    """
    template_name = 'community/question_list.html'
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
    queryset = Question.objects.all()

    # def get_object(self):
    #     return get_object_or_404(Question, pk=self.kwargs.get('pk', None))


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
                question.user = user
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


def question_update(request, pk):
    """
    최초 get 요청에서는 기존의 데이터를 보여주기 위해 Form(instance=question) 만 사용
    만약 request.POST, FILES 를 추가하면 모든 인스턴스를 초기화 상태로 두어
    DB 에서는 데이터가 있지만 유저가 봤을 때는 빈 폼으로 보여지는 상태를 가지게 됨
    """
    question = get_object_or_404(Question, pk=pk)
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = QuestionUpdateForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = user
            form.save()
            return redirect('community:questions')
    form = QuestionUpdateForm(instance=question)
    context = {
        'form': form
    }
    return render(request, 'community/question-create.html', context)


# class QuestionDeleteView(DeleteView):
#     """질문 게시판 글 삭제"""
#     model = Question
#     template_name = 'community/community_confirm_delete.html'
#
#     success_url = reverse_lazy('community:questions')
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         success_url = self.get_success_url()
#         if self.object.user == self.request.user:
#             self.object.delete()
#             return redirect('community:questions')
#         return redirect('community:questions')
#
#
# # 질문게시판 1개를 삭제하기 때문에 단수 question
# question_delete = QuestionDeleteView.as_view()


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
    """
    form 으로 처리하기 위해 POST 요청을 받고, FK 로 참조한 게시판(Question)이 있는지 확인
    Comment 모델에서 FK 로 User 를 참조하고 있기 때문에 user 인스턴스를 request.user.id 로 받아서 User 모델에서 해당 인스턴스를 참조
    form 을 저장하기 전에 commit=False 옵션으로 save() 를 잠시 대기 상태로 놓고 user 인스턴스를 생성되는 게시판 댓글의 user 로 할당
    (question 변수인 질문게시판도 동일 바로 윗줄의 내용과 동일한 흐름)
    """
    if request.method == 'POST':
        question = get_object_or_404(Question, pk=question_pk)
        # question = Question.objects.get(pk=question_pk)
        user = User.objects.get(pk=request.user.id)

        form = CommentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
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


class QuestionSearchListView(ListView):
    """
    템플릿에서도 name=q 를 qq 로 변경함
    현재 사이트에서 name=q 로 메인 검색(상품 검색)이 존재하기 때문에 다른 변수명을 주었음
    같은 변수명으로 할당하면 검색결과 기능에는 문제없지만 메인 검색에도 검색 텍스트가 존재함
    """
    model = Question
    queryset = Question.objects.all()
    template_name = 'community/question_result.html'

    def get_queryset(self):
        self.q = self.request.GET.get('qq', '')

        qs = super().get_queryset()
        if self.q:
            qs = qs.filter(
                Q(title__icontains=self.q) |
                Q(content__icontains=self.q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['qq'] = self.q
        return context


question_search_view = QuestionSearchListView.as_view()
