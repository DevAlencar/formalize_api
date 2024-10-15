class ChatBotStateMachine:
    def __init__(self, state='start'):
        self.state = state
    
    def handle_flow(self, user_input):
        # Mapeia o estado para o método correto
        state_handler = {
            'start': self._handle_start,
            'explain_cnpj': self._handle_explain_cnpj,
            'explain_cnpj_by_state': self._handle_explain_cnpj_by_state,
        }.get(self.state, self._handle_unknown_state)

        return state_handler(user_input)
    
    def _handle_start(self, user_input):
        if 'como abrir um cnpj' in user_input.lower():
            self.state = 'explain_cnpj'
            return (
                "Para abrir um CNPJ, você deve seguir os seguintes passos:\n"
                "1. Definir a natureza jurídica da empresa.\n"
                "2. Fazer o registro na Junta Comercial do seu estado.\n"
                "3. Realizar a inscrição no site da Receita Federal.\n"
                "Quer saber mais sobre como proceder no seu estado?", self.state
            )
        else:
            return "Desculpe, não entendi. Como posso te ajudar?", self.state

    def _handle_explain_cnpj(self, user_input):
        if 'sim' in user_input.lower():
            self.state = 'explain_cnpj_by_state'
            return (
                "Informe o estado que deseja ter melhores informações", self.state
            )
        else:
            self.state = 'start'
            return "Voltando ao menu principal", self.state
        


    def _handle_explain_cnpj_by_state(self, user_input):
        self.state = "start"
        state_links = {
            "São Paulo": "https://www.jucesp.sp.gov.br/",
            "Rio de Janeiro": "http://www.jucerja.rj.gov.br/",
            "Minas Gerais": "https://www.jucemg.mg.gov.br/",
            "Bahia": "http://www.juceb.ba.gov.br/",
            "Paraná": "http://www.juntacomercial.pr.gov.br/",
            "Rio Grande do Sul": "https://www.jucisrs.rs.gov.br/",
        }
        
        # Verifica se o usuário mencionou um estado e responde com o link apropriado
        for estado, link in state_links.items():
            print(estado)
            if estado.lower() in user_input.lower():
                resposta = f"Para abrir um CNPJ no estado de {estado}, visite a Junta Comercial: {link}."
                return resposta, self.state
        
        return "Desculpe, não entendi. Como posso te ajudar?", self.state 
          
    def _handle_unknown_state(self, user_input):
        return "Desculpe, ocorreu um erro. Pode repetir a sua pergunta?", 'start'
