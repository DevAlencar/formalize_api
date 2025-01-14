from django.db import models

class ViabilidadeEmpresa(models.Model):
    TIPO_JURIDICO_CHOICES = [
        ('EMP', 'Empresário'),
        ('SOC', 'Sociedade Empresária'),
        ('MEI', 'MEI'),
        ('SA', 'Sociedade Anônima'),
        ('COOP', 'Cooperativa'),
        ('CONS', 'Consórcio'),
        ('SOC_SIMP', 'Sociedade'),
    ]

    NATUREZA_JURIDICA_CHOICES = [
        ('LTDA', 'Sociedade empresária Ltda'),
        ('COL', 'Sociedade Empresária em nome coletivo'),
        ('CS', 'Sociedade Empresária em Comandita Simples'),
        ('CA', 'Sociedade Empresária em Comandita por Ações'),
        ('GS', 'Grupo de Sociedades'),
        ('SE', 'Estabelecimento, no Brasil, de Sociedade Estrangeira'),
        ('BIN', 'Estabelecimento, no Brasil, de empresa Binacional Argentino-Brasileira'),
    ]

    TIPO_UNIDADE_CHOICES = [
        ('PROD', 'Unidade Produtiva'),
        ('SEDE', 'Sede'),
        ('ESC', 'Escritório Administrativo'),
        ('DEP', 'Depósito Fechado'),
        ('ALM', 'Almoxarifado'),
        ('OFC', 'Oficina de Reparação'),
        ('GAR', 'Garagem'),
        ('COMB', 'Unidade de abastecimento de combustíveis'),
        ('EXP', 'Ponto de exposição'),
        ('TREI', 'Centro de treinamento'),
        ('CPD', 'Centro de Processamento de Dados'),
        ('COL', 'Posto de Coleta'),
    ]

    FORMA_ATUACAO_CHOICES = [
        ('FIXO', 'Estabelecimento Fixo'),
        ('INT', 'Internet'),
        ('FORA', 'Em Local Fixo Fora de Loja'),
        ('CORREIO', 'Correio'),
        ('PORTA', 'Porta a Porta, Postos Móveis ou por Ambulantes'),
        ('TELE', 'Televendas'),
        ('AUTO', 'Máquinas Automáticas'),
        ('EXT', 'Atividade Desenvolvida Fora do Estabelecimento'),
    ]

    ENQUADRAMENTO_CHOICES = [
        ('EPP', 'EPP - Empresa de Pequeno Porte'),
        ('ME', 'ME - Micro-empresa'),
        ('NORMAL', 'Normal ou outros enquadramentos'),
    ]

    CAPITAL_SOCIAL_CHOICES = [
        ('ESP', 'ESPÉCIE'),
        ('IMO', 'IMÓVEIS'),
        ('OUT', 'OUTROS'),
    ]

    # Pedido de Viabilidade
    municipio_interesse = models.CharField(max_length=100)
    is_matriz = models.BooleanField("É matriz?")
    is_filial = models.BooleanField("É filial?")
    inscricao_imobiliaria = models.CharField(max_length=50)
    area_estabelecimento = models.DecimalField(max_digits=10, decimal_places=2)
    inscricao_estadual = models.BooleanField("Solicita Inscrição Estadual?")
    
    # Tipos e Natureza
    tipo_juridico = models.CharField(max_length=10, choices=TIPO_JURIDICO_CHOICES)
    natureza_juridica = models.CharField(max_length=10, choices=NATUREZA_JURIDICA_CHOICES)
    tipo_unidade = models.CharField(max_length=10, choices=TIPO_UNIDADE_CHOICES)
    forma_atuacao = models.CharField(max_length=10, choices=FORMA_ATUACAO_CHOICES)
    
    # Endereço
    cep = models.CharField(max_length=8)
    uf = models.CharField(max_length=2)
    municipio = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    tipo_logradouro = models.CharField(max_length=50)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=200, blank=True)
    ponto_referencia = models.TextField(blank=True)

    # Nome Empresarial
    nome_empresarial = models.CharField(max_length=200)
    usar_cnpj_nome = models.BooleanField(default=False)

    # Objeto Social e CNAE
    objeto_social = models.TextField()
    cnae_principal = models.CharField(max_length=7)
    cnaes_secundarios = models.TextField(blank=True)

    # Informações Complementares
    enquadramento = models.CharField(max_length=10, choices=ENQUADRAMENTO_CHOICES)
    area_construida = models.DecimalField(max_digits=10, decimal_places=2)
    tem_habite_se = models.BooleanField("Possui Habite-se?")
    optante_simples = models.BooleanField("Optante pelo Simples Nacional?")
    telefone_contato = models.CharField(max_length=20)
    nome_contador = models.CharField(max_length=200)
    registro_bombeiros = models.CharField(max_length=50, blank=True)

    # Capital Social
    capital_social = models.DecimalField(max_digits=15, decimal_places=2)
    qtd_quotas = models.IntegerField()
    valor_quota = models.DecimalField(max_digits=15, decimal_places=2)
    tipo_capital = models.CharField(max_length=3, choices=CAPITAL_SOCIAL_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Socio(models.Model):
    viabilidade = models.ForeignKey(ViabilidadeEmpresa, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    is_administrador = models.BooleanField("É administrador?")
    endereco = models.TextField()
    qtd_quotas = models.IntegerField()
    
class Payment(models.Model):
    cliente_id = models.IntegerField()  # ID do cliente
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da transação
    status = models.CharField(max_length=50)  # Status do pagamento (approved, pending, etc.)
    created_at = models.DateTimeField(auto_now_add=True)  # Data e hora do registro