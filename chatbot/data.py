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
    "Alagoas": "https://www.sefaz.al.gov.br",
    "Amapá": "http://www.sefaz.ap.gov.br",
    "Amazonas": "https://online.sefaz.am.gov.br",
    "Bahia": "http://www.sefaz.ba.gov.br",
    "Ceará": "https://www.sefaz.ce.gov.br",
    "Distrito Federal": "http://www.fazenda.df.gov.br",
    "Espírito Santo": "https://internet.sefaz.es.gov.br",
    "Goiás": "http://www.sefaz.go.gov.br",
    "Maranhão": "https://sistemas.sefaz.ma.gov.br",
    "Mato Grosso": "http://www.sefaz.mt.gov.br",
    "Mato Grosso do Sul": "http://www.sefaz.ms.gov.br",
    "Minas Gerais": "https://www.sp.gov.br/sefaz",
    "Pará": "https://app.sefa.pa.gov.br",
    "Paraíba": "https://www.sefaz.pb.gov.br",
    "Paraná": "http://www.fazenda.pr.gov.br",
    "Pernambuco": "https://www.sefaz.pe.gov.br",
    "Piauí": "https://www.sefaz.pi.gov.br",
    "Rio de Janeiro": "http://www.fazenda.rj.gov.br",
    "Rio Grande do Norte": "http://www.set.rn.gov.br",
    "Rio Grande do Sul": "https://www.sefaz.rs.gov.br",
    "Rondônia": "https://portalcontribuinte.sefin.ro.gov.br",
    "Roraima": "https://www.sefaz.rr.gov.br",
    "Santa Catarina": "https://www.sef.sc.gov.br",
    "São Paulo": "https://efisco.sefaz.sp.gov.br",
    "Sergipe": "https://www.sefaz.se.gov.br",
    "Tocantins": "http://www.sefaz.to.gov.br"
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
