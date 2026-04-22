from django.contrib import admin
from .models import Empresa, Vaga, Candidatura

@admin.register(Empresa)  #Ele diz que a classe abaixo servirá para customizar como o modelo Empresa aparece no painel
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email_contato', 'criado_em')  #tabela organizada com o Nome, o E-mail e a Data de Criação lado a lado.
    search_fields = ('nome',)  #barra de pesquisa

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'salario', 'criado_em', 'ativo') 
    list_filter = ('empresa', 'criado_em', 'ativo')  #filtros rápidos
    search_fields = ('titulo', 'descricao')  

@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'vaga', 'criado_em')
    readonly_fields = ('criado_em',) #Força o Django a mostrar a data no formulário
                                     #pq o Django por padrão o esconderia

