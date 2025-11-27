class SistemaArquivos:
    def __init__(self, total_blocos):
        self.total_blocos = total_blocos
        # Mapa do disco: None = livre, NomeArquivo = ocupado
        self.disco = [None] * total_blocos
        # Tabela de arquivos: Nome -> {criador: PID, inicio: int, tamanho: int}
        self.arquivos = {}

    def inicializar_disco(self, arquivos_iniciais):
        """Inicializa o disco com arquivos pré-existentes"""
        # arquivos_iniciais: lista de (nome, inicio, tamanho)
        for nome, inicio, tamanho in arquivos_iniciais:
            if inicio + tamanho <= self.total_blocos:
                self._gravar_disco(inicio, tamanho, nome)
                self.arquivos[nome] = {'criador': None, 'inicio': inicio, 'tamanho': tamanho} # None = sistema/root
            else:
                print(f"Erro: Arquivo {nome} excede tamanho do disco.")

    def criar_arquivo(self, processo, nome, tamanho):
        """Cria um arquivo usando First-Fit"""
        if nome in self.arquivos:
            print(f"Erro: Arquivo {nome} já existe.")
            return False

        # Busca First-Fit
        contador_livres = 0
        indice_inicio_livre = -1

        for i in range(self.total_blocos):
            if self.disco[i] is None:
                if contador_livres == 0:
                    indice_inicio_livre = i
                contador_livres += 1
                
                if contador_livres == tamanho:
                    # Aloca
                    self._gravar_disco(indice_inicio_livre, tamanho, nome)
                    self.arquivos[nome] = {'criador': processo.pid, 'inicio': indice_inicio_livre, 'tamanho': tamanho}
                    print(f"Processo {processo.pid} criou arquivo '{nome}' (Blocos {indice_inicio_livre}-{indice_inicio_livre+tamanho-1}).")
                    return True
            else:
                contador_livres = 0
                indice_inicio_livre = -1
        
        print(f"Processo {processo.pid} falhou ao criar arquivo '{nome}' (Sem espaço).")
        return False

    def deletar_arquivo(self, processo, nome):
        """Deleta arquivo verificando permissões"""
        if nome not in self.arquivos:
            print(f"Erro: Arquivo {nome} não existe.")
            return False

        info = self.arquivos[nome]
        
        # Regras de permissão:
        # RT (Prio 0): Pode deletar qualquer coisa
        # User (Prio > 0): Só pode deletar o que criou
        pode_deletar = False
        if processo.tipo == 'RT':
            pode_deletar = True
        elif info['criador'] == processo.pid:
            pode_deletar = True
        
        if pode_deletar:
            self._limpar_disco(info['inicio'], info['tamanho'])
            del self.arquivos[nome]
            print(f"Processo {processo.pid} deletou arquivo '{nome}'.")
            return True
        else:
            print(f"Processo {processo.pid} negado ao deletar '{nome}' (Permissão insuficiente).")
            return False

    def _gravar_disco(self, inicio, tamanho, valor):
        for i in range(inicio, inicio + tamanho):
            self.disco[i] = valor

    def _limpar_disco(self, inicio, tamanho):
        for i in range(inicio, inicio + tamanho):
            self.disco[i] = None

    def imprimir_mapa(self):
        print("\n--- Mapa do Disco ---")
        mapa_visual = ""
        for i, bloco in enumerate(self.disco):
            val = bloco if bloco else "0"
            mapa_visual += f"[{val}]"
        print(mapa_visual)
        print("---------------------\n")
