from django.contrib import admin

from .models import Community, CommentCommunity

admin.site.register(Community)

admin.site.register(CommentCommunity)
