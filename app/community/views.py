from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views.generic import CreateView

from .models import Community, CommentCommunity
from .forms import CommunityCreateForm, CommentCreateForm


User = get_user_model()


def community_notice_list(request):
    community_list = Community.objects.all()
    context = {
        'community_list': community_list,
    }
    return render(request, 'community/main_notice.html', context)


def community_detail(request, community_pk):
    community_detail = Community.objects.get(pk=community_pk)
    comment_list = CommentCommunity.objects.filter(community_id=community_detail.pk)
    context = {
        'community_detail': community_detail,
        'comment_list': comment_list,
    }
    return render(request, 'community/community_detail.html', context)


@login_required
def community_create(request):
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        # form 을 받을 때 request.POST, request.FILES 순서대로 정의해야 함
        # form.is_valid() 상태여도 데이터가 unbound 상태
        form = CommunityCreateForm(request.POST, request.FILES)
        if user is not None:
            if form.is_valid():
                community = form.save(commit=False)
                community.user = request.user
                community.title = form.cleaned_data['title']
                community.content = form.cleaned_data['content']
                community.image = form.cleaned_data['image']
                form.save()
                return redirect('community:notice')
    else:
        form = CommunityCreateForm()
        context = {
            'form': form,
        }
        return render(request, 'community/notice-create.html', context)


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
def comment_create(request, community_pk):
    if request.method == 'POST':
        community = Community.objects.get(pk=community_pk)
        # community = CommentCommunity.objects.get(community_id=community_pk)

        form = CommentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.community = community
            comment.content = form.cleaned_data['content']
            comment.image = form.cleaned_data['image']
            form.save()
            return redirect('community:detail', community.pk)

    form = CommentCreateForm()
    context = {
        'form': form,
    }
    return render(request, 'community/comment-create.html', context)
