from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model): #Aplicando o conceito DRY
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True) # Campo para o Soft Delete

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
    nome = models.CharField(max_length=100)
    site = models.URLField(blank=True)  # O site é opcional (blank=True)
    email_contato = models.EmailField()

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

class Candidatura(BaseModel):
    # Relacionamento com o usuário do Django e com a Vaga
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='candidatos')
    mensagem = models.TextField(help_text="Fale um pouco sobre sua experiência")

    class Meta:
        # Evita que o mesmo usuário se candidate duas vezes na mesma vaga
        unique_together = ('usuario', 'vaga')

    def __str__(self):
        return f"{self.usuario.username} -> {self.vaga.titulo}"
