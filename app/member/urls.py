from django.urls import path

from member.views import signup_view, login_view

app_name = 'members'
urlpatterns = [
    path('', signup_view, name='signup'),
    path('login/', login_view, name='login'),
]