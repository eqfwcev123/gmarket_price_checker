from django.urls import path

from member.views import login_view, signup_view

app_name = 'members'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='login'),
]