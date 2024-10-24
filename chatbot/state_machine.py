class ChatBotStateMachine:
    def __init__(self, state='menu'):
        self.state = state

    
    def handle_flow(self, user_input):
        # Mapeia o estado para o método correto
        state_handler = {
            'menu': self._handle_menu,
            'explain_certidoes': self._handle_explain_certidoes,
            'certidao_sefaz': self._handle_certidao_sefaz,
        }.get(self.state, self._handle_unknown_state)

        return state_handler(user_input)
    
    def _handle_menu(self, user_input):
       
        # '1':'Abrir cnpj',
        # '2':'Emitir certidões',
        
        # Menu inicial de opções
        if '1' in user_input.lower():
            self.state = 'start_cnpj_process'
            answer = "Para abrir um CNPJ, você deve seguir os seguintes passos:"
            questions = [
                {"body": "Definir a natureza jurídica da empresa"},
                {"body": "Fazer o registro na Junta Comercial do seu estado"},
                {"body": "Realizar a inscrição no site da Receita Federal"},
                {"body": "Deseja saber mais sobre algum estado específico?"},
                {"body": "Deseja voltar ao menu inicial?"}
            ]
            return answer, questions, self.state
        elif '2' in user_input.lower():
            self.state = 'explain_certidoes'
            answer = "Existem várias certidões negativas que podem ser emitidas, sobre qual deseja saber mais?"
            questions = [
                {"body": "Certidão da Receita Federal"},
                {"body": "Certidão da SEFAZ (ICMS)"},
                {"body": "Certidão de Regularidade Fiscal"},
                {"body": "Certidão FGTS"},
                {"body": "Certidão Trabalhista"},
                {"body": "Certidão Municipal"},
                {"body": "Certidão de Antecedentes Criminais"}
            ]
            return answer, questions, self.state

    def _handle_explain_certidoes(self, user_input):
        certidoes = {
            '1': 'certidao_receita_federal',
            '2': 'certidao_sefaz',
            '3': 'certidao_regularidade_fiscal',
            '4': 'certidao_fgts',
            '5': 'certidao_trabalhista',
            '6': 'certidao_municipal',
            '7': 'certidao_antecedentes_criminais'
        }
        if user_input in certidoes.keys():
            self.state = 'menu'
                
            if certidoes[user_input] == 'certidao_receita_federal':
                link = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/EmitirPGFN"
                answer = f"Aqui está o link para emitir a Certidão da Receita Federal: {link}"
                questions = [
                    {"body": "Desejo retornar ao menu inicial"}
                ]
                return answer, questions, self.state
            
            elif certidoes[user_input] == 'certidao_sefaz':
                self.state = 'certidao_sefaz'
                return "Informe o estado que deseja buscar", [], self.state

            elif certidoes[user_input] == 'certidao_regularidade_fiscal':
                link = "https://efisco.sefaz.pe.gov.br/sfi_trb_gcc/PREmitirCertidaoRegularidadeFiscal"
                answer = f"Aqui está o link para emitir a Certidão de Regularidade Fiscal: {link}"
                questions = [
                    {"body": "Desejo retornar ao menu inicial"}
                ]
                return answer, questions, self.state

            elif certidoes[user_input] == 'certidao_fgts':
                link = "https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf"
                answer = f"Aqui está o link para emitir a Certidão FGTS: {link}"
                questions = [
                    {"body": "Desejo retornar ao menu inicial"}
                ]
                return answer, questions, self.state


            elif certidoes[user_input] == 'certidao_trabalhista':
                link = "https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf"
                answer = f"Aqui está o link para emitir a Certidão Trabalhista: {link}"
                questions = [
                    {"body": "Desejo retornar ao menu inicial"}
                ]
                return answer, questions, self.state

            elif certidoes[user_input] == 'certidao_municipal':
                link = "https://cndt-certidao.tst.jus.br/inicio.faces"
                answer = f"Aqui está o link para emitir a Certidão Municipal: {link}"
                questions = [
                    {"body": "Desejo retornar ao menu inicial"}
                ]
                return answer, questions, self.state

            elif certidoes[user_input] == 'certidao_antecedentes_criminais':
                link = "https://www.tjpe.jus.br/antecedentescriminaiscliente/xhtml/manterPessoa/tipoPessoa.xhtml"
                answer = f"Aqui está o link para emitir a Certidão de Antecedentes Criminais: {link}"
                questions = [
                    {"body": "Desejo retornar ao menu inicial"}
                ]
                return answer, questions, self.state
        else:
            self.state = 'menu'
            return "Desculpe, não entendi. Voltando ao menu inicial.", [], self.state

    def _handle_certidao_sefaz(self, user_input):
        self.state = 'menu'
        sefaz_links = {
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

        link = sefaz_links.get(user_input, "Link não encontrado para o estado informado.")

        if link != "Link não encontrado para o estado informado.":
            answer = f"Aqui está o link para emitir a Certidão da SEFAZ no estado de {user_input}: {link}"
            questions = [
                {"body": "Desejo retornar ao menu inicial"}
            ]
        else:
            answer = "Desculpe, não encontramos o link para o estado informado."
            questions = [
                {"body": "Desejo retornar ao menu inicial"},
                {"body": "Desejo tentar outro estado"}
            ]

        return answer, questions, self.state
    
    
    def _handle_unknown_state(self, user_input):
        self.state = 'menu'
        return "Desculpe, ocorreu um erro. Voltando ao menu inicial.", [], self.state
