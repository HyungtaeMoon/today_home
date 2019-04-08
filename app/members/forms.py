from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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


class SignupForm(forms.Form):
    CHOICE_GENDER = (
        ('man', '남성'),
        ('woman', '여성')
    )
    username = forms.CharField(
        label='사용자 아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    email = forms.CharField(
        label='이메일',
        widget=forms.EmailInput(
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
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    alias = forms.CharField(
        label='닉네임',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    gender = forms.CharField(
        label='성별',
        widget=forms.Select(
            choices=CHOICE_GENDER,
            attrs={
                'class': 'form-control',
            }
        )
    )
    profile_img = forms.FileField(
        label='프로필 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    cover_img = forms.FileField(
        label='커버 이미지',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    introduce = forms.CharField(
        label='자기소개',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def cleaned_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise ValidationError('이미 사용중인 아이디 입니다.')
        return data

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            self.add_error('password2', '비밀번호와 비밀번호 확인 값이 일치하지 않습니다.')
        return self.cleaned_data

    def signup(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return user


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
