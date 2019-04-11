from django.contrib.auth import get_user_model
from django.shortcuts import render

from .models import Community, CommentCommunity


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


# def community_create(request):
#     if request.method == 'POST':
#         user = User.objects.get(pk=request.user.id)
#         if user is not None:
#             pass
