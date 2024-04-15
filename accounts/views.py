from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
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


class UserProfileView(DetailView):
    model = User
    template_name = "accounts/{username}.html"

    def get_object(self, queryset=None):
        username=self.kwargs.get("username")
        return self.request.user
