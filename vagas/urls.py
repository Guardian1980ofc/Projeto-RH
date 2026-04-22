from django.urls import path
from . import views

urlpatterns = [
    # Públicas / Entrada
    path('', views.HomeView.as_view(), name='home'),
    path('vagas/', views.VagaListView.as_view(), name='vaga_list'),
    
    # Login (Identificação)
    path('login/candidato/', views.LoginCandidatoView.as_view(), name='login_candidato'),
    path('login/empresa/', views.LoginEmpresaView.as_view(), name='login_empresa'),
    
    # CRUD Empresa (O motor do sistema)
    path('vaga/nova/', views.VagaCreateView.as_view(), name='vaga_create'),
    path('vaga/<int:pk>/editar/', views.VagaUpdateView.as_view(), name='vaga_update'),
    path('vaga/<int:pk>/remover/', views.VagaDeleteView.as_view(), name='vaga_delete'),
]
