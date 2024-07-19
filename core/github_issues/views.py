from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View

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

    def post(self, request):
        form = RepositoryForm(request.POST)
        queryset = Repository.objects.filter(user=request.user).select_related('user')
        if form.is_valid():
            new_repo = form.save(commit=False)
            new_repo.user = request.user
            new_repo.save()

            context = {
                'form': form,
                'repositories': queryset,
            }
            return redirect('issues')
        else:
            return redirect('issues')

