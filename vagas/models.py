from django.db import models
from django.contrib.auth.models import User

# O Porteiro Especializado
class ActiveManager(models.Manager):
    def get_queryset(self):
        # Sempre filtra para retornar apenas o que está ativo=True
        return super().get_queryset().filter(ativo=True)

class BaseModel(models.Model): #Aplicando o conceito DRY
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True) # Campo para o Soft Delete

    # Definindo os Gerenciadores (Managers)
    objects = models.Manager() # Manager padrão (acessa tudo)
    active = ActiveManager()   # Manager customizado (acessa só ativos)

    class Meta:
        abstract = True

    def delete(self):
        """Sobrescreve o método delete para apenas desativar o registro"""
        self.ativo = False
        self.save()

    def hard_delete(self):
        """O delete definitivo(CUIDADO)"""
        super(BaseModel, self).delete()

class Empresa(BaseModel):  #Ele não depende de ninguém, mas outros dependerão dele.
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empresa', null=True, blank=True)
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18)
    site = models.URLField(blank=True)  # O site é opcional (blank=True)
    email_contato = models.EmailField(unique=True)

    def __str__(self):
        return self.nome

class Vaga(BaseModel):
    # Relacionamento 1:N (Uma empresa tem várias vagas)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='vagas')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.titulo} - {self.empresa.nome}"

class Candidatura(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidatos')
    nome_candidato = models.CharField(max_length=100)
    cpf_candidato = models.CharField(max_length=14)
    data_candidatura = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Candidatura"
        verbose_name_plural = "Candidaturas"
        # Impede o mesmo CPF de se inscrever na mesma vaga
        unique_together = ('vaga', 'cpf_candidato')

    def __str__(self):
        return f"{self.nome_candidato} -> {self.vaga.titulo}"
