from django.urls import path

from member.views import signup_view, login_view, logout_view

app_name = 'members'
urlpatterns = [
    path('', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]