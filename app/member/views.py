# Create your views here.
from django.shortcuts import render

from member.forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        pass
    else:
        form = LoginForm()
        context = {
            'loginForm': form
        }
    return render(request, 'members/login.html', context)


def signup_view(request):
    pass
