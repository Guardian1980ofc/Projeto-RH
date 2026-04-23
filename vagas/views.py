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

# --- OBSERVAÇÃO ARQUITETURAL: USO DE FUNCTION-BASED VIEWS (FBV) ---
# Optei por utilizar FBVs para os fluxos de identificação (Empresa e Candidato)
# por oferecerem controle total e explícito sobre o ciclo de requisição/resposta.
#
# 1. No Login da Empresa: Facilita a autenticação customizada cruzando dados 
#    da tabela Empresa (CNPJ/E-mail) com o modelo User padrão.
# 2. No Login do Candidato: Permite a persistência de dados via request.session 
#    sem a necessidade imediata de persistência em banco de dados, tornando o 
#    fluxo de candidatura mais ágil e menos burocrático.
# Esse controle granular é mais intuitivo em FBVs do que sobrescrever múltiplos 
# métodos de uma Class-Based View (CBV) padrão de login.

def login_candidato(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')
        
        if cpf and nome:
            # Salvamos o CPF e o Nome na sessão do navegador
            # Assim não precisamos de uma tabela de 'Candidato' agora
            request.session['candidato_cpf'] = cpf
            request.session['candidato_nome'] = nome
            messages.success(request, f"Olá {nome}, você já pode se candidatar às vagas!")
            return redirect('vaga_list')
        else:
            messages.error(request, "Preencha o nome e o CPF para continuar.")
            
    return render(request, 'vagas/login_candidato.html')

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
    logout(request) # Limpa o login da empresa
    request.session.flush() # Limpa o CPF e Nome do candidato da sessão
    messages.info(request, "Você saiu com sucesso!")
    return redirect('home')
