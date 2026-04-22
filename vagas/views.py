from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import Vaga


class HomeView(TemplateView):
    template_name = 'vagas/home.html'


class VagaListView(ListView):
    model = Vaga
    template_name = 'vagas/index.html'
    context_object_name = 'vagas'

    def get_queryset(self):
        # Aqui usamos o nosso "Porteiro" para mostrar apenas as vagas ATIVAS
        return Vaga.active.all().order_by('-criado_em')


