from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic import CreateView, TemplateView
from .models import Client, Result
from .forms import RegisterForm, LoginForm, TelegramIdForm
from django.contrib import messages


# Create your views here.

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'client/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        Client.objects.create(user_ptr_id=user.id, telegram_id='')
        login(self.request, user)
        return super().form_valid(form)


class GinLoginView(LoginView):
    form_class = LoginForm
    template_name = 'client/login.html'
    next_page = reverse_lazy('index')


class GinLogoutView(LogoutView):
    next_page = reverse_lazy('index')


class IndexView(TemplateView):
    template_name = 'client/home.html'


@method_decorator(login_required, name='dispatch')
class GinProfileView(View):
    template_name = 'client/profile.html'
    def get(self, request):
        form = TelegramIdForm()
        queryset = Result.objects.filter(client=request.user.client).select_related('client')
        context = {
            'form': form,
            'results': queryset,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = TelegramIdForm(request.POST)
        if form.is_valid():
            telegram_id = form.cleaned_data['telegram_id']
            client = request.user.client
            client.telegram_id = telegram_id
            client.save()
            messages.success(request, "Telegram ID was successfully updated!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the error below.")
            queryset = Result.objects.filter(client=request.user.client).select_related('client')
            context = {
                'form': form,
                'results': queryset,
            }
            return render(request, self.template_name, context)
