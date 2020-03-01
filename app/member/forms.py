from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

from member.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="사용자 아이디", widget=forms.TextInput(
        attrs={
            'class': 'form-input',
            'placeholder': '아이디'
        }))
    password = forms.CharField(label='사용자 비밀번호', widget=forms.PasswordInput(
        attrs={
            'class': 'form-input',
            'placeholder': '비밀번호'
        }
    ))

    # is_valid() 호출시 clean() 자동 호출. clean() 함수를 오버라이딩
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("아이디 혹은 비밀번호를 잘못 입력하셨습니다.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        login(request, user)


class SignupForm(forms.Form):
    username = forms.CharField(
        label='사용자 아이디',
        widget=forms.TextInput(
            attrs={
                'class': 'username-field',
                'placeholder': '아이디',
            }
        ))
    password = forms.CharField(
        label='사용자 비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'password-field',
                'placeholder': '비밀번호',
            }
        ))
    email = forms.EmailField(
        label='사용자 이메일',
        widget=forms.EmailInput(
            attrs={
                'class': 'email-field',
                'placeholder': '이메일',
            }
        ))
    name = forms.CharField(
        label='이름',
        widget=forms.TextInput(
            attrs={
                'class': 'name-field',
                'placeholder': '이름',
            }
        ))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('이미 사용중인 username입니다')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('이미 사용중인 email입니다')
        return email

    def save(self):
        User.objects.create(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            name=self.cleaned_data['name']
        )
