from django.urls import path
from .views import HomeView, VagaListView

urlpatterns = [
    # Página de Boas-vindas
    path('', HomeView.as_view(), name='home'),
    
    # Página de Lista de Vagas 
    path('vagas/', VagaListView.as_view(), name='vaga_list'),
]
