from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('성공적으로 인증됨')
                else:
                    return HttpResponse('비활성화된 계정')
            else:
                return HttpResponse('유효하지 않은 로그인')
        else:
            form = LoginForm()
    return render(request, 'account/login.html')