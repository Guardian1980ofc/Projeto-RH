from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Vaga

# --- VIEWS PÚBLICAS / CANDIDATO ---

class HomeView(TemplateView):
    template_name = 'vagas/home.html'

class VagaListView(ListView):
    model = Vaga
    template_name = 'vagas/index.html'
    context_object_name = 'vagas'

    def get_queryset(self):
        # Aqui usamos o nosso "Porteiro" para mostrar apenas as vagas ATIVAS
        return Vaga.active.all().order_by('-criado_em')

# --- VIEWS DE LOGIN (SISTEMA DE ESCOLHA) ---

class LoginCandidatoView(TemplateView):
    template_name = 'vagas/login_candidato.html' # Login via CPF

class LoginEmpresaView(TemplateView):
    template_name = 'vagas/login_empresa.html' # Login via CNPJ

# --- CRUD DA EMPRESA (GERENCIAMENTO) ---

class VagaCreateView(CreateView):
    model = Vaga
    template_name = 'vagas/vaga_form.html'
    fields = ['titulo', 'descricao', 'salario', 'empresa'] # Campos que a empresa vai preencher
    success_url = reverse_lazy('vaga_list') # Para onde volta depois de criar

class VagaUpdateView(UpdateView):
    model = Vaga
    template_name = 'vagas/vaga_form.html'
    fields = ['titulo', 'descricao', 'salario', 'ativo']
    success_url = reverse_lazy('vaga_list')

    def get_queryset(self):
        # AQUI ESTÁ A SEGURANÇA:
        # Ele só vai permitir editar se a vaga pertencer à empresa logada
        base_queryset = super().get_queryset()
        return base_queryset.filter(empresa=self.request.user.empresa)

class VagaDeleteView(DeleteView):
    model = Vaga
    template_name = 'vagas/vaga_confirm_delete.html'
    success_url = reverse_lazy('vaga_list')

    def get_queryset(self):
        # AQUI ESTÁ A SEGURANÇA:
        # A mesma trava que a de editar
        return super().get_queryset().filter(empresa=self.request.user.empresa)
