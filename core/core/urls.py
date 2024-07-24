"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from client import views
from github_issues.views import GinRepositoryView, GinDeleteRepo, GinUpdateRepo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.GinLoginView.as_view(), name='login'),
    path('logout/', views.GinLogoutView.as_view(), name='logout'),
    path('profile/', views.GinProfileView.as_view(), name='profile'),
    path('issues/', GinRepositoryView.as_view(), name='issues'),
    path('add/', create_repository, name='add'),
    path('<int:pk>/delete/', GinDeleteRepo.as_view(), name='delete'),
    path('<int:pk>/update/', GinUpdateRepo.as_view(), name='update'),
    path('', views.IndexView.as_view(), name='index')
]
