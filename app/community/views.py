from django.shortcuts import render

from .models import Community


def community_notice_list(request):
    community_list = Community.objects.all()
    context = {
        'community_list': community_list,
    }
    return render(request, 'community/main_notice.html', context)
