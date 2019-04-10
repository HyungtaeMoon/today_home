from django.shortcuts import render

from .models import Community


def community_notice_list(request):
    community_list = Community.objects.all()
    context = {
        'community_list': community_list,
    }
    return render(request, 'community/main_notice.html', context)


def community_detail(request, community_pk):
    community_detail = Community.objects.get(pk=community_pk)
    context = {
        'community_detail': community_detail,
    }
    print(context)
    return render(request, 'community/community_detail.html', context)
