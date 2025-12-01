class Processo:
    def __init__(self, pid, tipo, prioridade, tempo_execucao, blocos_memoria, recursos_necessarios=None, operacoes_io=None, tempo_inicio=0):
        self.pid = pid
        self.tipo = tipo  # 'RT' ou 'USER'
        self.prioridade = prioridade
        self.tempo_execucao = tempo_execucao
        self.blocos_memoria = blocos_memoria
        self.recursos_necessarios = recursos_necessarios if recursos_necessarios else []
        self.operacoes_io = operacoes_io if operacoes_io else []
        self.tempo_restante = tempo_execucao
        self.tempo_espera = 0
        self.tempo_inicio = tempo_inicio

        # Estado do sistema
        self.offset = None
        self.recursos_alocados = False  # NOVO: Flag para controle de recursos
        
        # Flags para o dispatcher (apenas visualização)
        self.usa_scanner = False
        self.usa_impressora = 0
        self.usa_modem = False
        self.usa_sata = 0
        
        self.quantum = self._definir_quantum(prioridade)

    def _definir_quantum(self, prioridade):
        tabela_quantum = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2}
        return tabela_quantum.get(prioridade, 0)

    def atualizar_prioridade(self, nova_prioridade):
        if self.tipo == 'USER':
            self.prioridade = nova_prioridade
            self.quantum = self._definir_quantum(nova_prioridade)

    def __repr__(self):
        return f"[PID: {self.pid} | Tipo: {self.tipo} | Prio: {self.prioridade} | Mem: {self.blocos_memoria}]"