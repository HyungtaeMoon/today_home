import imghdr
import io
import json
from pprint import pprint

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect


from .forms import SignupForm, LoginForm, UserProfileForm

User = get_user_model()


@login_required
def profile(request):
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        # pk 나 username 등으로 식별할 수 있는 정보를 매개변수로 받지 않기 때문에
        #   instance=request.user 로 유저를 판단
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('members:profile')
    form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'members/profile.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            # 유저가 authenticate 검증에 통과할 경우,
            if user is not None:
                # 세션값을 만들어 DB 에 저장, 쿠키에 해당값을 담아 보내는 로그인 함수로 로그인
                login(request, user)
                return redirect('product:home')
            else:
                return redirect('members:login')
    else:
        # 모든 get 요청으로 접근하면 LoginForm 의 빈 양식을 렌더링
        #   즉, URL 을 통한 get 요청, 로그인 버튼을 통한 리다이렉트도 모두 아래의 form 을 거쳐감
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'members/login.html', context)


@login_required
def logout_view(request):
        logout(request)
        return redirect('product:category-list')


def signup_view(request):
    """UserCreationForm 을 사용"""
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            # name = form.cleaned_data['name']
            # alias = form.cleaned_data['alias']
            # gender = form.cleaned_data['gender']
            # profile_img = form.cleaned_data['profile_img']
            # cover_img = form.cleaned_data['cover_img']
            # introduce = form.cleaned_data['introduce']
            user = authenticate(request, email=email, password=password1)
            login(request, user)
            return redirect('product:category-list')

    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'members/signup.html', context)


def facebook_login(request):
    api_base = 'https://graph.facebook.com/v3.3'
    api_get_access_token = f'{api_base}/oauth/access_token?'
    api_me = f'{api_base}/me'

    code = request.GET.get('code')
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': 'http://localhost:8000/members/facebook-login/',
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'code': code,
    }
    response = requests.get(api_get_access_token, params)
    response_object = json.loads(response.text)
    data = response.json()
    access_token = data['access_token']

    params = {
        'access_token': access_token,
        'fields': ','.join([
            'id',
            'name',
            'picture.type(large)',
        ])
        # 'fields': 'id, name, picture'
    }

    response = requests.get(api_me, params)
    data = response.json()

    facebook_id = data['id']
    facebook_at = '@facebook.id'
    name = data['name']
    url_img_profile = data['picture']['data']['url']

    img_response = requests.get(url_img_profile)
    img_data = img_response.content

    # f = io.BytesIO(img_response.content)

    ext = imghdr.what('', h=img_data)
    f = SimpleUploadedFile(f'{facebook_id}.{ext}', img_response.content)

    try:
        user = User.objects.get(email=facebook_id + facebook_at)
        user.name = name
        # user.profile_img = f
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=facebook_id + facebook_at,
            name=name,
            profile_img=f,
        )
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    # pprint(data)
    # return HttpResponse(str(data))
    return redirect('product:home')
