from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(
        label='아이디',
        widget=forms.TextInput(
            attrs={
                'placeholder': '아이디 (이메일 형식)',
                'class': 'form-control',
            }
        )
    )
    password = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호',
                'class': 'form-control',
            }
        )
    )


class SignupForm(UserCreationForm):
    CHOICE_GENDER = (
        ('man', '남자'),
        ('woman', '여자')
    )
    email = forms.EmailField(label='아이디(이메일 형식)')
    name = forms.CharField(max_length=10, label='이름')
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    alias = forms.CharField(max_length=50, label='닉네임')
    gender = forms.CharField(label='성별', widget=forms.Select(choices=CHOICE_GENDER))
    profile_img = forms.ImageField(label='프로필 이미지(선택)', widget=forms.ClearableFileInput(), required=False)
    cover_img = forms.ImageField(label='커퍼 이미지(선택)', widget=forms.ClearableFileInput(), required=False)
    introduce = forms.CharField(label='자기소개', widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'name', 'alias',
                  'gender', 'profile_img', 'cover_img', 'introduce']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        # field 의 모든 템플릿 속성에 class=form-control 적용
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'alias',
            'gender',
            'profile_img',
            'cover_img',
            'introduce'
        ]
        widget = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'name': forms.TextInput(
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
