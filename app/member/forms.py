from django import forms


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
