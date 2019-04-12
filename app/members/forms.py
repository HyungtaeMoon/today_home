from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        label='사용자 아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class SignupForm(UserCreationForm):
    CHOICE_GENDER = (
        ('man', '남자'),
        ('woman', '여자')
    )
    username = forms.CharField(max_length=30, label='아이디')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    alias = forms.CharField(max_length=50, label='닉네임')
    gender = forms.CharField(label='성별', widget=forms.Select(choices=CHOICE_GENDER))
    profile_img = forms.ImageField(label='프로필 이미지(선택)', widget=forms.ClearableFileInput(), required=False)
    cover_img = forms.ImageField(label='커퍼 이미지(선택)', widget=forms.ClearableFileInput(), required=False)
    introduce = forms.CharField(label='자기소개', widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'alias',
                  'gender', 'profile_img', 'cover_img', 'introduce']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'alias',
            'gender',
            'profile_img',
            'cover_img',
            'introduce'
        ]
        widget = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'alias': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'profile_img': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'cover_img': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'introduce': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }
