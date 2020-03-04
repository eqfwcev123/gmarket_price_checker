# Create your views here.
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect
from member.forms import LoginForm, SignupForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('shop:shopping-list')
    else:
        form = LoginForm()
    print(request.user)
    context = {
        'loginForm': form
    }
    return render(request, 'members/login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('shop:shopping-list')
    else:
        form = SignupForm()
    context = {
        'signupForm': form
    }
    return render(request, 'members/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('members:login')