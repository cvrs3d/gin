from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .tasks import fetch_labels_task, search_issues_task
from .forms import RepositoryForm
from .models import Repository


# Create your views here.
@method_decorator(login_required, name='dispatch')
class GinRepositoryView(ListView):
    template_name = 'github_issues/issues_list.html'
    model = Repository

    def get(self, request, *args, **kwargs):
        queryset = Repository.objects.filter(user=request.user).select_related('user')
        context = {'repositories': queryset}
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class GinAddNewRepo(CreateView):
    model = Repository
    form_class = RepositoryForm
    template_name = 'github_issues/create_repo.html'
    success_url = reverse_lazy('issues')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            repository = form.save(commit=False)
            repository.user = request.user
            repository.save()
            repo_id = repository.pk
            fetch_labels_task.delay(repo_id)
        return redirect(self.success_url)


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
    template_name = 'github_issues/search_issues.html'

    def get(self, request):
        repositories = Repository.objects.filter(user=request.user).select_related('user')
        return render(request, self.template_name, {
            "repositories": repositories
        })

    def post(self, request):
        repo_id = request.POST.get('repo_id')
        labels = request.POST.getlist('labels')
        user_id = request.user.id
        search_issues_task.delay(repo_id, labels, user_id)
        return redirect('profile')
