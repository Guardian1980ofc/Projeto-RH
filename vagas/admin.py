from django.contrib import admin
from .models import Empresa, Vaga, Candidatura

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email_contato', 'criado_em', 'ativo')
    search_fields = ('nome', 'cnpj')
    list_filter = ('ativo',)

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'empresa', 'salario', 'criado_em', 'ativo')
    list_filter = ('empresa', 'criado_em', 'ativo')
    search_fields = ('titulo', 'descricao')

@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = ('nome_candidato', 'cpf_candidato', 'vaga', 'data_candidatura')
    search_fields = ('nome_candidato', 'cpf_candidato')
    list_filter = ('vaga', 'data_candidatura')