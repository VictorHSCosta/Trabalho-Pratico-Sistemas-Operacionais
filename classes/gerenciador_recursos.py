class GerenciadorRecursos:
    def __init__(self):
        # Recursos disponíveis
        self.recursos = {
            'SCANNER': 1,
            'IMPRESSORA': 2,
            'MODEM': 1,
            'SATA': 3
        }
        # Controle de alocação: PID -> Lista de recursos alocados
        self.alocados = {} 

    def verificar_disponibilidade(self, recursos_solicitados):
        """Verifica se há recursos suficientes para atender a solicitação"""
        # Conta quantos de cada recurso são necessários
        contagem = {}
        for rec in recursos_solicitados:
            contagem[rec] = contagem.get(rec, 0) + 1
            
        for rec, qtd in contagem.items():
            if self.recursos.get(rec, 0) < qtd:
                return False
        return True

    def alocar(self, processo):
        """Tenta alocar recursos para o processo. Retorna True se sucesso."""
        recursos_solicitados = processo.recursos_necessarios
        if not recursos_solicitados:
            return True # Não precisa de nada

        if self.verificar_disponibilidade(recursos_solicitados):
            for rec in recursos_solicitados:
                self.recursos[rec] -= 1
            
            self.alocados[processo.pid] = list(recursos_solicitados)
            return True
        return False

    def liberar(self, processo):
        """Libera os recursos alocados para o processo"""
        recursos_do_processo = self.alocados.get(processo.pid, [])
        if recursos_do_processo:
            for rec in recursos_do_processo:
                self.recursos[rec] += 1
            del self.alocados[processo.pid]
            return True
        return False
