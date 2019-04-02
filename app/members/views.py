from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignupForm, LoginForm, UserProfileForm

User = get_user_model()


@login_required
def profile(request):
    if request.method == 'POST':
        # pk 나 username 등으로 식별할 수 있는 정보를 매개변수로 받지 않기 때문에
        #   instance=request.user 로 유저를 판단
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
    form = UserProfileForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'members/profile.html', context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            # 유저가 authenticate 검증에 통과할 경우,
            if user is not None:
                # 세션값을 만들어 DB 에 저장, 쿠키에 해당값을 담아 보내는 로그인 함수로 로그인
                login(request, user)
                return redirect('product:category-list')
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
    if request.method == 'POST':
        # form 을 채우고 POST 요청을 보냈을 때 이 구간이 실행됨
        #   form 에 POST 가 바인드 됨(request 의 POST 정보가 들어옴)
        #   form 의 바인드 된 인스턴스를 request.POST 를 사용하여 form 으로 인스턴스화
        form = SignupForm(request.POST, request.FILES)

        # form 에 대한 정보가 설정한 필드의 조건에 맞다면(True),
        #   예를들면 이메일 필드에 이메일 주소로 입력을 했다면 통과
        if form.is_valid():
            # Signupform 에 정의되어 있는 signup 메서드를 호출
            user = form.signup()
            # 세션값을 만들어 DB 에 저장, 쿠키에 해당값을 담아 보냄
            login(request, user)
            return redirect('product:category-list')

    else:
        # GET 요청(회원가입 버튼 클릭, url 직접 접근) 등은
        #   비어있는 SignupForm 을 생성
        form = SignupForm()
    # POST 요청으로 채워진 폼도 아래의 context 에 채워지고,
    #   GET 요청으로 온 폼도 아래의 context(빈 form) 으로 채워 렌더링
    context = {
        'form': form,
    }
    return render(request, 'members/signup.html', context)
