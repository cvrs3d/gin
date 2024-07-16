from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import RegisterForm, LoginForm


# Create your views here.

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'client/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class GinLoginView(LoginView):
    form_class = LoginForm
    template_name = 'client/login.html'
    success_url = reverse_lazy('home')


class GinLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class IndexView(TemplateView):
    template_name = 'client/home.html'
