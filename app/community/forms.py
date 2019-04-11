from django import forms

from .models import Community


class CommunityCreateForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = [
            'title',
            'content',
            'image'
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
            ),
        }
