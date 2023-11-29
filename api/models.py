from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.cidade}/{self.estado} - CEP: {self.cep}'
    
    
# class Cadastro(models.Model):
#     def upload_imagem_cliente(instance, filename):
#         return f"{instance.conta}-{filename}"
    
#     nome = models.CharField(max_length=50)
#     nasc = models.CharField(max_length=50)
#     cpf = models.IntegerField()
#     # rg = models.CharField(max_length=20, default='')
#     # telefone = models.CharField(max_length=15, default='')
#     endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True)  
#     email = models.EmailField(unique=True)
#     senha = models.CharField(max_length=50)
#     # conta = models.CharField(max_length=10, unique=True, default='')
#     # criado_em = models.DateTimeField(default='')
#     # agencia = models.CharField(max_length=10,  default='0000')
#     # renda = models.CharField(max_length=10,  default='')
#     imagem = models.ImageField(upload_to=upload_imagem_cliente, blank=True, null=True) 
    
#     def __str__(self):
#         return f'{self.nome} - {self.email} - {self.imagem} - {self.criado_em}'
    
    

class Cadastro(models.Model):
    nome = models.CharField(max_length=50)
    nasc = models.CharField(max_length=50)
    cpf = models.IntegerField()
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True)  
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.nome} - {self.email}'
    
 
class Login(models.Model):
    
    email = models.ForeignKey(Cadastro, on_delete=models.CASCADE, related_name='logins_email')
    senha = models.OneToOneField(Cadastro, on_delete=models.CASCADE, related_name='login_senha')
    
    def __str__(self):
        return f'{self.email} - {self.senha}'
    
    
class Cliente(models.Model):
    
    def upload_imagem_cliente(instance, filename):
        return f"{instance.conta}-{filename}"

    nome = models.ForeignKey(Cadastro, null=True, verbose_name='nome_cliente', related_name='nome', on_delete=models.PROTECT)
    conta = models.CharField(max_length=10, unique=True, default='')
    limite = models.FloatField(null=True)
    agencia = models.CharField(max_length=10)
    renda = models.CharField(max_length=10,  default='')
    # criado_em = models.DateTimeField(auto_now_add=True)
    ultima_movimentacao = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to=upload_imagem_cliente, blank=True, null=True)

    def __str__(self):
        return f'{self.nome} - {self.imagem}'
    
    
    
class Transacao(models.Model):

    conta_cliente = models.ForeignKey(Cliente, null=True, verbose_name='Cliente', related_name='transacoes',on_delete=models.PROTECT)
    descricao = models.CharField(max_length=120, null=False)
    valor = models.FloatField(null=False)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.conta_cliente


class Contas(models.Model):
    cliente = models.OneToOneField('Cliente', on_delete=models.CASCADE)
    saldo = models.DecimalField(decimal_places=2, max_digits=30, default=0.00)
    
    def __str__(self) :
        return f'{str(self.cliente)}/{str(self.saldo)}'
    
    def get_ultima_movimentacao(self):
        return self.ultima_movimentacao.strftime('%d/%m/%Y %H:%M')
    
    # def get_saldo(self):
    #     return self.saldo
    
    
# class Saldo(models.Model):
#     cliente = models.OneToOneField('Cliente', on_delete=models.CASCADE, related_name='saldo_associado')
#     saldo = models.DecimalField(max_digits=10, decimal_places=2)
#     ultima_movimentacao = models.DateTimeField()
    
#     def __str__(self):
#         return f'{self.cliente} - R$ {self.saldo}'


class Deposito(models.Model):
    conta = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    data_deposito = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{str(self.conta)}'
    
    def get_data_deposito(self):
        return self.data_deposito.strftime('%d/%m/%Y %H:%M')
    
    
class Saque(models.Model):
    conta = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    data_saque = models.DateTimeField(auto_now_add=True)
    
    def get_data_saque(self):
        return self.data_saque.strftime('%d/%m/%Y %H:%M')
    
@receiver(post_save, sender=Deposito)
def update_saldo(sender, instance, **kwargs):
    instance.conta.saldo += instance.valor
    instance.conta.save()
    
@receiver(post_save, sender=Saque)
def update_saldo(sender, instance, **kwargs):
    instance.conta.saldo -= instance.valor
    instance.conta.save()
        
        
        
class Emprestimo(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    valor = models.FloatField()
    taxa_juros = models.FloatField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Empréstimo de {self.valor} para {self.cliente}'
    
    
class Credito(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    renda = models.FloatField()
    
    def __str__(self):
        return self.cliente
