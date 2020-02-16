from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError


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
            raise ValidationError("아이디 혹은 비밀번호를 잘못 입력하셨 습니다.")
        return self.cleaned_data

    def login(self,request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        login(request,user)
