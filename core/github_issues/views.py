from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import RepositoryForm
from .models import Repository


# Create your views here.

class GinRepositoryView(View):
    template_name = 'github_issues/issues_list.html'

    def get(self, request):
        queryset = Repository.objects.filter(user=request.user).select_related('user')
        form = RepositoryForm()
        context = {
            'form': form,
            'repositories': queryset
        }
        return render(request, self.template_name, context)


class GinAddNewRepo(CreateView):
    model = Repository
    fields = ['name', 'url', 'issue']
    template_name = 'github_issues/add_issue.html'
    success_url = '/issues/'

    def form_valid(self, form):
        new_repo = form.save(commit=False)
        new_repo.user = self.request.user
        new_repo.save()

        return super().form_valid(form)


class GinDeleteRepo(DeleteView):
    model = Repository
    success_url = reverse_lazy('issues')


class GinUpdateRepo(UpdateView):
    model = Repository
    fields = ['name', 'url', 'issue']
    template_name = 'github_issues/update.html'
    success_url = reverse_lazy('issues')

