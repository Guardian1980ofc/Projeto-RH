from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Vaga, Empresa 

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

# OBSERVAÇÃO TÉCNICA: Optei por Function-Based View para o login da empresa 
# devido à necessidade de uma autenticação customizada (CNPJ/E-mail).
# Diferente das CBVs padrões, a FBV oferece controle total e explícito sobre o 
# processamento do POST, facilitando a validação de campos que não pertencem 
# ao modelo de usuário padrão do Django.
def login_empresa(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        cnpj = request.POST.get('cnpj')
        
        # Busca a empresa pelo e-mail e cnpj
        empresa = Empresa.objects.filter(email_contato=email, cnpj=cnpj).first()
        
        if empresa and empresa.usuario:
            login(request, empresa.usuario)
            messages.success(request, f"Bem-vindo, {empresa.nome}!")
            return redirect('vaga_list')
        else:
            messages.error(request, "E-mail ou CNPJ não encontrados.")
            
    return render(request, 'vagas/login_empresa.html')

# --- CRUD DA EMPRESA (GERENCIAMENTO) ---

# Adicionei LoginRequiredMixin para garantir que só logados acessem
class VagaCreateView(LoginRequiredMixin, CreateView):
    model = Vaga
    template_name = 'vagas/vaga_form.html'
    fields = ['titulo', 'descricao', 'salario'] # Campos que a empresa vai preencher
    success_url = reverse_lazy('vaga_list') # Para onde volta depois de criar
    login_url = 'login_empresa'

    # Já diz qual empresa cria a vaga
    def form_valid(self, form):
        form.instance.empresa = self.request.user.empresa
        return super().form_valid(form)

class VagaUpdateView(LoginRequiredMixin, UpdateView):
    model = Vaga
    template_name = 'vagas/vaga_form.html'
    fields = ['titulo', 'descricao', 'salario', 'ativo']
    success_url = reverse_lazy('vaga_list')
    login_url = 'login_empresa'

    def get_queryset(self):
        # AQUI ESTÁ A SEGURANÇA:
        # Ele só vai permitir editar se a vaga pertencer à empresa logada
        base_queryset = super().get_queryset()
        return base_queryset.filter(empresa=self.request.user.empresa)

class VagaDeleteView(LoginRequiredMixin, DeleteView):
    model = Vaga
    template_name = 'vagas/vaga_confirm_delete.html'
    success_url = reverse_lazy('vaga_list')
    login_url = 'login_empresa'

    def get_queryset(self):
        # AQUI ESTÁ A SEGURANÇA:
        # A mesma trava que a de editar
        return super().get_queryset().filter(empresa=self.request.user.empresa)
    
class VagaDetailView(DetailView):
    model = Vaga
    template_name = 'vagas/vaga_detail.html'
    context_object_name = 'vaga'

def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu com sucesso!")
    return redirect('home')
