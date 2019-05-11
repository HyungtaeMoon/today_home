from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import User


# class UserAdmin(BaseUserAdmin):
#     fieldsets = (
#         (None, {
#             'fields': (
#                 'email',
#                 'password',
#             ),
#         }),
#         ('개인정보', {
#             'fields': (
#                 'profile_img',
#             ),
#         }),
#     )


admin.site.register(User)
