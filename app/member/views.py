# Create your views here.
from django.shortcuts import render, redirect

from member.forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            form.login(request)

        return redirect('shop:shopping-list')
    else:
        form = LoginForm()
    context = {
        'loginForm': form
    }
    return render(request, 'members/login.html', context)


def signup_view(request):
    return render(request, 'members/signup.html')
