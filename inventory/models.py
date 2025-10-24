# inventory/models.py
from django.db import models
from django.contrib.auth.models import User # Sistema de usuários do Django
from django.utils import timezone
import os

# --- Opções baseadas no seu config.py ---
# Convertido para o formato de 'choices' do Django: (valor_banco, valor_legivel)
CENTER_COST_OPTIONS = [
    ("101 - Puxada", "101 - Puxada"),
    ("202 - Armazém", "202 - Armazém"),
    ("301 - Administrativo", "301 - Administrativo"),
    ("401 - Vendas", "401 - Vendas"),
    ("501 - Entrega", "501 - Entrega"),
    ("601 - CSC", "601 - CSC"),
]

REVENDAS_OPTIONS = [
    ("Revalle Juazeiro", "Revalle Juazeiro"),
    ("Revalle Bonfim", "Revalle Bonfim"),
    ("Revalle Petrolina", "Revalle Petrolina"),
    ("Revalle Ribeira", "Revalle Ribeira"),
    ("Revalle Paulo Afonso", "Revalle Paulo Afonso"),
    ("Revalle Alagoinhas", "Revalle Alagoinhas"),
    ("Revalle Serrinha", "Revalle Serrinha"),
]

TIPO_EQUIPAMENTO_CHOICES = [
    ("", "Selecione um tipo..."), # Opção vazia para o formulário dinâmico
    ("Celular", "Celular"),
    ("Notebook", "Notebook"),
    ("Desktop", "Desktop"),
    ("Impressora", "Impressora"),
    ("Tablet", "Tablet"),
    ("Switch", "Switch"),
    ("HD", "HD"),
    ("Nobreak", "Nobreak"),
    ("Access Point", "Access Point"),
]

class Peripheral(models.Model):
    """ Tradução da sua tabela 'peripherals' """
    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Em Uso', 'Em Uso'),
        ('Substituido', 'Substituido'),
    ]
    
    tipo = models.CharField(max_length=50, null=False)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    identificador = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível')
    motivo_substituicao = models.CharField(max_length=255, blank=True, null=True)
    date_registered = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        # Isso define como o objeto aparece no Admin do Django
        return f"{self.tipo} {self.brand} ({self.identificador or 'S/N'})"

class Item(models.Model):
    """ Tradução da sua tabela 'items' """
    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Indisponível', 'Indisponível'),
        ('Pendente', 'Pendente'),
        ('Pendente Devolução', 'Pendente Devolução'),
    ]
    
    POE_CHOICES = [('Sim', 'Sim'), ('Não', 'Não')]

    tipo = models.CharField(max_length=50, blank=True, null=True, choices=TIPO_EQUIPAMENTO_CHOICES)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    identificador = models.CharField(max_length=100, blank=True, null=True)
    nota_fiscal = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível')
    
    # --- Dados do Empréstimo ---
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    revenda = models.CharField(max_length=100, choices=REVENDAS_OPTIONS, blank=True, null=True)
    
    # --- Dados Técnicos ---
    dominio = models.CharField(max_length=50, blank=True, null=True)
    host = models.CharField(max_length=100, blank=True, null=True)
    endereco_fisico = models.CharField(max_length=150, blank=True, null=True)
    cpu = models.CharField(max_length=100, blank=True, null=True)
    ram = models.CharField(max_length=50, blank=True, null=True)
    storage = models.CharField(max_length=50, blank=True, null=True)
    sistema = models.CharField(max_length=100, blank=True, null=True)
    licenca = models.CharField(max_length=100, blank=True, null=True)
    anydesk = models.CharField(max_length=50, blank=True, null=True)
    setor = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True, null=True)
    mac = models.CharField(max_length=50, blank=True, null=True)
    fornecedor = models.CharField(max_length=150, blank=True, null=True)
    potencia_nominal = models.CharField(max_length=50, blank=True, null=True)
    autonomia_estimada = models.CharField(max_length=100, blank=True, null=True)
    ip_snmp = models.CharField(max_length=50, blank=True, null=True)
    codigo_patrimonial = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    local_instalacao = models.CharField(max_length=150, blank=True, null=True)
    poe = models.CharField(max_length=3, choices=POE_CHOICES, blank=True, null=True)
    quantidade_portas = models.CharField(max_length=10, blank=True, null=True)
    
    # --- Datas ---
    date_registered = models.DateTimeField(default=timezone.now)
    date_issued = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # --- O VÍNCULO! (Tradução da 'equipment_peripherals') ---
    # Isso cria a tabela de junção automaticamente para você.
    peripherals = models.ManyToManyField(
        Peripheral,
        blank=True, # Um item pode ter zero periféricos
        related_name="equipment" 
    )

    def __str__(self):
        return f"ID {self.id}: {self.tipo} {self.brand} ({self.status})"

class History(models.Model):
    """ Tabela de histórico de operações """
    OPERATION_CHOICES = [
        ('Cadastro', 'Cadastro'),
        ('Empréstimo', 'Empréstimo'),
        ('Devolução', 'Devolução'),
        ('Edição', 'Edição'),
        ('Exclusão', 'Exclusão'),
        ('Estorno', 'Estorno'),
        ('Confirmação Empréstimo', 'Confirmação Empréstimo'),
        ('Confirmação Devolução', 'Confirmação Devolução'),
        ('Cadastro Periférico', 'Cadastro Periférico'),
        ('Vínculo Periférico', 'Vínculo Periférico'),
        ('Desvínculo Periférico', 'Desvínculo Periférico'),
        ('Substituição Periférico', 'Substituição Periférico'),
    ]

    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    peripheral = models.ForeignKey(Peripheral, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Seu 'operador' agora é uma chave estrangeira para o usuário real do Django
    operador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    usuario = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    center_cost = models.CharField(max_length=100, blank=True, null=True)
    setor = models.CharField(max_length=100, blank=True, null=True)
    fornecedor = models.CharField(max_length=150, blank=True, null=True)
    revenda = models.CharField(max_length=100, blank=True, null=True)
    data_operacao = models.DateTimeField(default=timezone.now)
    operation = models.CharField(max_length=30, choices=OPERATION_CHOICES, default='Cadastro')
    is_reversed = models.BooleanField(default=False)
    details = models.CharField(max_length=255, blank=True, null=True)

    # --- Campos para log de itens/periféricos excluídos ---
    tipo = models.CharField(max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    identificador = models.CharField(max_length=100, blank=True, null=True)
    nota_fiscal = models.CharField(max_length=50, blank=True, null=True)
    poe = models.CharField(max_length=3, blank=True, null=True)
    quantidade_portas = models.CharField(max_length=10, blank=True, null=True)

    # --- Anexos ---
    # O Django gerenciará o upload desses arquivos para pastas específicas
    operacao_anexo = models.FileField(upload_to='anexos/operacoes/', blank=True, null=True)
    termo_assinado_anexo = models.FileField(upload_to='anexos/termos/', blank=True, null=True)

    def __str__(self):
        return f"{self.operation} em {self.data_operacao.strftime('%d/%m/%Y')}"