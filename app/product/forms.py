from django import forms

from .models import Comment


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'rating',
            'content',
            'image',
        ]


class CommentUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'rating',
            'content',
            'image'
        ]


class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'rating',
            'content',
            'image'
        ]


# class CommentDeleteForm(forms.Form):
#     RATING_CHOICES = (
#         (1, '재구매 의사 없어요(1점)'),
#         (2, '별로에요(2점)'),
#         (3, '나쁘지 않아요(3점)'),
#         (4, '구매 의사 있어요(4점)'),
#         (5, '주변 사람에게 추천해요(5점)')
#     )
#     rating = forms.ChoiceField(
#         choices=RATING_CHOICES,
#         widget=forms.IntegerField,
#         required=True)
#
#     content = forms.CharField(
#         widget=forms.Textarea(
#             attrs={
#                 'rows': 5,
#                 'cols': 20
#             }
#         )
#     )
#     image = forms.ImageField(
#         widget=forms.ClearableFileInput()
#     )
