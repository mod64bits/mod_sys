from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'