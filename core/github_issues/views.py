from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from tasks import fetch_labels_task, search_issues_task
from .forms import RepositoryForm
from .models import Repository


# Create your views here.
@method_decorator(login_required, name='dispatch')
class GinRepositoryView(ListView):
    template_name = 'github_issues/issues_list.html'
    model = Repository

    def get_queryset(self):
        queryset = Repository.objects.filter(user=self.request.user).select_related('user')
        return queryset


@method_decorator(login_required, name='dispatch')
class GinAddNewRepo(CreateView):
    model = Repository
    form_class = RepositoryForm
    template_name = 'github_issues/create_repo.html'
    success_url = '/issues/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        fetch_labels_task.delay(self.object.id)
        return response


@method_decorator(login_required, name='dispatch')
class GinDeleteRepo(DeleteView):
    model = Repository
    success_url = reverse_lazy('issues')


@method_decorator(login_required, name='dispatch')
class GinUpdateRepo(UpdateView):
    model = Repository
    fields = ['name', 'owner', 'url']
    template_name = 'github_issues/update.html'
    success_url = reverse_lazy('issues')

    def form_valid(self, form):
        response = super().form_valid(form)
        fetch_labels_task.delay(self.object.id)
        return response


@method_decorator(login_required, name='dispatch')
class SearchIssueView(View):
    template_name = 'github_issues/search_form.html'

    def get(self, request):
        repositories = Repository.objects.filter(user=request.user).select_related('user')
        return render(request, self.template_name, {
            "repositories": repositories
        })

    def post(self, request):
        repo_id = request.POST.get('repo_id')
        labels = request.POST.get('labels')
        search_issues_task.delay(repo_id, labels)
        return JsonResponse({'status': '900 - search started'})
