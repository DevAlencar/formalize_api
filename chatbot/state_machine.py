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
            return (
                "Para abrir um CNPJ, você deve seguir os seguintes passos:\n"
                "1. Definir a natureza jurídica da empresa.\n"
                "2. Fazer o registro na Junta Comercial do seu estado.\n"
                "3. Realizar a inscrição no site da Receita Federal.\n"
                "Deseja saber mais sobre algum estado específico ou deseja voltar ao menu inicial?", self.state
            )
        elif '2' in user_input.lower():
            self.state = 'explain_certidoes'
            return (
                "Existem várias certidões negativas que podem ser emitidas. "
                "Deseja saber sobre:\n"
                "1. Certidão da Receita Federal\n"
                "2. Certidão da SEFAZ (ICMS)\n"
                "3. Certidão de Regularidade Fiscal\n"
                "4. Certidão FGTS\n"
                "5. Certidão Trabalhista\n"
                "6. Certidão Municipal\n"
                "7. Certidão de Antecedentes Criminais\n"
                "Por favor, escolha uma opção (número ou nome).", self.state
            )
        else:
            return "Desculpe, não entendi. Como posso te ajudar?", self.state

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
        print(certidoes)
        if user_input in certidoes.keys():
            self.state = 'menu'
                
            if certidoes[user_input] == 'certidao_receita_federal':
                link = "https://solucoes.receita.fazenda.gov.br/Servicos/certidaointernet/PJ/EmitirPGFN"
                return f"Aqui está o link para emitir a Certidão da Receita Federal: {link}", self.state
            
            elif certidoes[user_input] == 'certidao_sefaz':
                self.state = 'certidao_sefaz'
                return f"Informe o estado que deseja buscar", self.state
            
            elif certidoes[user_input] == 'certidao_regularidade_fiscal':
                link = "https://efisco.sefaz.pe.gov.br/sfi_trb_gcc/PREmitirCertidaoRegularidadeFiscal"
                return f"Aqui está o link para emitir a Certidão de Regularidade Fiscal: {link}", self.state
            
            elif certidoes[user_input] == 'certidao_fgts':
                link = "https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf"
                return f"Aqui está o link para emitir a Certidão FGTS: {link}", self.state

            elif certidoes[user_input] == 'certidao_trabalhista':
                link = "https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf"
                return f"Aqui está o link para emitir a Certidão FGTS: {link}", self.state
            
            elif certidoes[user_input] == 'certidao_municipal':
                link = "https://cndt-certidao.tst.jus.br/inicio.faces"
                return f"Aqui está o link para emitir a Certidão Trabalhista: {link}", self.state
            
            elif certidoes[user_input] == 'certidao_antecedentes_criminais':
                link = "https://www.tjpe.jus.br/antecedentescriminaiscliente/xhtml/manterPessoa/tipoPessoa.xhtml"
                return f"Aqui está o link para emitir a Certidão de Antecedentes Criminais: {link}", self.state
        else:
            self.state = 'menu'
            return "Desculpe, não entendi. Voltando ao menu inicial.", self.state

    def _handle_certidao_sefaz(self, user_input):
        self.state = 'menu'
        sefaz_links = {
            "São Paulo": "https://efisco.sefaz.sp.gov.br/",
            "Minas Gerais": "https://www.sp.gov.br/sefaz",
            # Adicionar mais estados conforme necessário
        }
        link = sefaz_links.get(user_input, "Link não encontrado para o estado informado.")
        return f"Aqui está o link para emitir a Certidão da SEFAZ no estado de {user_input}: {link}", self.state
    
    
    def _handle_unknown_state(self, user_input):
        self.state = 'menu'
        return "Desculpe, ocorreu um erro. Voltando ao menu inicial.", self.state
