from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from django.conf import settings

from .forms import SignupForm

User = get_user_model()


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "accounts/login.html"

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy(settings.LOGIN_REDIRECT_URL, kwargs={"username": username})


class UserProfileView(DetailView):
    model = User
    template_name = "accounts/{username}.html"

    def get_object(self, queryset=None):
        return self.get_queryset().get(username=self.kwargs["username"])
