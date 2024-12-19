# chatbot/data.py
from typing import Dict, List

CERTIDOES_LINKS: Dict[str, str] = {
    'receita_federal': 'https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/EmitirPGFN',
    'regularidade_fiscal': 'https://efisco.sefaz.pe.gov.br/sfi_trb_gcc/PREmitirCertidaoRegularidadeFiscal',
    'fgts': 'https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf',
    'trabalhista': 'https://cndt-certidao.tst.jus.br/inicio.faces',
    'municipal': 'https://servicos.sefaz.recife.pe.gov.br/',
    'antecedentes criminais': 'https://www.tjpe.jus.br/antecedentescriminaiscliente/xhtml/manterPessoa/tipoPessoa.xhtml',
    'antecedentes_criveis': 'https://www.tjpe.jus.br/certidaopje/xhtml/main.xhtml',
}

SEFAZ_LINKS: Dict[str, str] = {
    "Acre": "http://www.sefaz.ac.gov.br",
    # ... rest of states
}

MENU_OPTIONS: Dict[str, List[str]] = {
    'main': [
        "Abrir CNPJ",
        "Emitir certidões"
    ],
    'certidoes': [
        "Certidão da Receita Federal",
        "Certidão da SEFAZ (ICMS)",
        "Certidão de Regularidade Fiscal", 
        "Certidão FGTS",
        "Certidão Trabalhista",
        "Certidão Municipal",
        "Certidão de Antecedentes Criminais",
        "Antecedentes Criveis"
    ]
}
