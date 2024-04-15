# from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path('login/', LoginView.as_view(template_name="accounts/login.html",form_class=AuthenticationForm ), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('<str:username>/', views.UserProfileView.as_view(template_name="{username}.html"), name='user_profile'),
    # path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    # path('<str:username>/unfollow/', views.UnFollowView, name='unfollow'),
    # path('<str:username>/following_list/', views.FollowingListView.as_view(), name='following_list'),
    # path('<str:username>/follower_list/', views.FollowerListView.as_view(), name='follower_list'),
]
