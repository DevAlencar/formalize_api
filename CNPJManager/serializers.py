from rest_framework import serializers
from .models import ViabilidadeEmpresa, Socio

class SocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socio
        fields = ['cpf', 'is_administrador', 'endereco', 'qtd_quotas']

class ViabilidadeEmpresaSerializer(serializers.ModelSerializer):
    socios = SocioSerializer(many=True, required=False)

    class Meta:
        model = ViabilidadeEmpresa
        fields = [
            'municipio_interesse',
            'is_matriz',
            'is_filial',
            'inscricao_imobiliaria',
            'area_estabelecimento',
            'inscricao_estadual',
            'tipo_juridico',
            'natureza_juridica',
            'tipo_unidade',
            'forma_atuacao',
            'cep',
            'uf',
            'municipio',
            'bairro',
            'tipo_logradouro',
            'logradouro',
            'numero',
            'complemento',
            'ponto_referencia',
            'nome_empresarial',
            'usar_cnpj_nome',
            'objeto_social',
            'cnae_principal',
            'cnaes_secundarios',
            'enquadramento',
            'area_construida',
            'tem_habite_se',
            'optante_simples',
            'telefone_contato',
            'nome_contador',
            'registro_bombeiros',
            'capital_social',
            'qtd_quotas',
            'valor_quota',
            'tipo_capital',
            'socios'
        ]

    def validate(self, data):
        if data.get('capital_social') and data.get('qtd_quotas') and data.get('valor_quota'):
            if data['capital_social'] != (data['qtd_quotas'] * data['valor_quota']):
                raise serializers.ValidationError(
                    "O capital social deve ser igual ao produto da quantidade de quotas pelo valor unitário"
                )
        return data

    def create(self, validated_data):
        socios_data = validated_data.pop('socios', [])
        viabilidade = ViabilidadeEmpresa.objects.create(**validated_data)
        
        for socio_data in socios_data:
            Socio.objects.create(viabilidade=viabilidade, **socio_data)
        
        return viabilidade