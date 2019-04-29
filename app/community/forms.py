from django import forms

from .models import Question, CommentQuestion


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'title',
            'content',
            'image',
        ]
        labels = {
            'title': '제목',
            'content': '내용',
            'image': '사진추가',
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '제목을 적어주세요',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '내용을 적어주세요. \n참고가 되는 사진을 공유해주시면 더 좋은 답변을 얻으실 수 있습니다.'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = CommentQuestion
        fields = [
            'content',
            'image',
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

# class CommentCreateForm(forms.Form):
#     content = forms.CharField(
#         widget=forms.Textarea(
#             attrs={
#                 'class': 'form-control',
#                 'row': 3,
#             }
#         )
#     ),
#
#     # def save(self, community, **kwargs):
#     #     content = self.cleaned_data['content']
#     #     return community.comments.create(
#     #         content=content,
#     #         **kwargs,
#     #     )
#
#     def clean(self):
#         cleaned_data = super(CommentCreateForm, self).clean()
#         content = cleaned_data.get('content')
#         if not content:
#             raise forms.ValidationError('You have to write something!')
