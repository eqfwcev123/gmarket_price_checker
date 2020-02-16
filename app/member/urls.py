from django.urls import path

from member.views import login_view, signup_view

app_name = 'members'
urlpatterns = [
    path('', signup_view, name='signup'),
    path('login/', login_view, name='login'),
]