class GerenciadorMemoria:
    def __init__(self):
        self.total_blocos = 1024
        self.blocos_rt = 64
        self.blocos_user = 960
        # Mapa de memória: None = livre, PID = ocupado
        self.memoria = [None] * self.total_blocos

    def alocar(self, processo):
        blocos_necessarios = processo.blocos_memoria
        
        if processo.tipo == 'RT':
            inicio_busca = 0
            fim_busca = self.blocos_rt
        else:
            inicio_busca = self.blocos_rt
            fim_busca = self.total_blocos

        # Busca First-Fit por blocos contíguos
        contador_livres = 0
        indice_inicio_livre = -1

        for i in range(inicio_busca, fim_busca):
            if self.memoria[i] is None:
                if contador_livres == 0:
                    indice_inicio_livre = i
                contador_livres += 1
                
                if contador_livres == blocos_necessarios:
                    # Encontrou espaço suficiente, aloca
                    self._preencher_memoria(indice_inicio_livre, blocos_necessarios, processo.pid)
                    processo.offset = indice_inicio_livre
                    return True
            else:
                contador_livres = 0
                indice_inicio_livre = -1
        
        return False

    def desalocar(self, processo):
        pid = processo.pid
        desalocou = False
        for i in range(self.total_blocos):
            if self.memoria[i] == pid:
                self.memoria[i] = None
                desalocou = True
        if desalocou:
            processo.offset = None
        return desalocou

    def _preencher_memoria(self, inicio, tamanho, pid):
        for i in range(inicio, inicio + tamanho):
            self.memoria[i] = pid
