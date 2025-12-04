from collections import deque
from utils.saida import imprimir_despacho 
from classes.processo import Processo

class Escalonador:
    def __init__(self, gerenciador_recursos=None, sistema_arquivos=None, gerenciador_memoria=None):
        self.fila_global = deque()
        self.fila_rt = deque()
        self.filas_usuario = {1: deque(), 2: deque(), 3: deque(), 4: deque(), 5: deque()}
        self.tempo_limite_aging = 10
        self.max_processos = 100
        
        self.gerenciador_recursos = gerenciador_recursos
        self.sistema_arquivos = sistema_arquivos
        self.gerenciador_memoria = gerenciador_memoria # Agora precisamos da memória aqui

    # Se a fila global ainda tiver espaco, adiciona o processo
    def adicionar_processo(self, processo):
        limite_memoria = 64 if processo.tipo == 'RT' else 960
    
        if processo.blocos_memoria > limite_memoria:
            print(f"ERRO CRÍTICO: Processo {processo.pid} rejeitado. Requisita {processo.blocos_memoria} blocos (Máx permitido: {limite_memoria}).")
            return  # Não adiciona na fila, descarta o processo imediatamente
        if len(self.fila_global) + self._total_processos_ativos() < self.max_processos:
            self.fila_global.append(processo)
        else:
            print(f"Erro: Capacidade máxima atingida para PID {processo.pid}.")

    def _total_processos_ativos(self):
        count = len(self.fila_rt)
        for fila in self.filas_usuario.values():
            count += len(fila)
        return count

    def distribuir_processos(self):
        """Move processos da fila global para prontos se houver memória."""
        # Usamos uma lista auxiliar para não quebrar o loop ao remover da fila_global
        nao_alocados = []
        
        while self.fila_global:
            proc = self.fila_global.popleft()
            
            # Tenta alocar memória. Se conseguir, entra na fila de execução.
            # Se não conseguir, volta para fila global.
            if self.gerenciador_memoria.alocar(proc):
                if proc.tipo == 'RT':
                    self.fila_rt.append(proc)
                    print(f"Processo {proc.pid} (RT) carregado na memória e pronto.")
                else:
                    prio = max(1, min(5, proc.prioridade))
                    proc.atualizar_prioridade(prio)
                    self.filas_usuario[prio].append(proc)
                    print(f"Processo {proc.pid} (User) carregado na memória e pronto.")
            else:
                print(f"Processo {proc.pid} aguardando memória...")
                nao_alocados.append(proc)
        
        # Volta os processos que não foram alocados para a fila global
        for proc in reversed(nao_alocados):
            self.fila_global.appendleft(proc)

    def executar(self):
        print("\n--- Iniciando Execução do Escalonador ---\n")
        
        while self._existem_processos():
            self.distribuir_processos()
            self.aplicar_aging()

            # Primeiro executamos a fila de real time
            if self.fila_rt:
                self._executar_rt()
                continue 

            # Depois executamos as filas de usuário
            executou_usuario = False
            for prio in range(1, 6):
                if self.filas_usuario[prio]:
                    self._executar_usuario(prio)
                    executou_usuario = True
                    break
            
            if not executou_usuario and not self.fila_rt and not self.fila_global:
                break # Encerra se não há nada rodando nem aguardando

        print("\n--- Todos os processos finalizados ---")

    def _executar_rt(self):
        proc = self.fila_rt[0] # RT é FIFO, não removemos até terminar
        
        # Imprime despacho padrão
        imprimir_despacho(proc)
        
        # Simula execução completa (RT não sofre preempção)
        print(f"process {proc.pid} =>")
        print(f"P{proc.pid} STARTED (RT)")
        
        instrucao_inicial = proc.tempo_execucao - proc.tempo_restante + 1
        for i in range(instrucao_inicial, proc.tempo_execucao + 1):
            print(f"P{proc.pid} instruction {i}")
            
            # I/O simples (se houver lógica implementada)
            if self.sistema_arquivos:
                self._executar_operacoes_io(proc)

        print(f"P{proc.pid} return SIGINT")
        
        # Finalização
        self.fila_rt.popleft()
        self.gerenciador_memoria.desalocar(proc)
        # RT não aloca recursos no gerenciador de recursos neste exemplo, 
        # ou assume-se que já tem prioridade total.

    def _executar_usuario(self, prio_atual):
        fila = self.filas_usuario[prio_atual]
        proc = fila.popleft()

        # 1. Tenta alocar recursos se ainda não tem
        if proc.recursos_necessarios and not proc.recursos_alocados:
            if not self.gerenciador_recursos.alocar(proc):
                print(f"P{proc.pid} bloqueado por recursos. Retornando à fila.")
                fila.append(proc) # Bloqueio simples (volta pro fim da fila)
                return
            else:
                proc.recursos_alocados = True

        imprimir_despacho(proc)
        
        # Primeira execucão de um processo
        if proc.tempo_restante == proc.tempo_execucao:
             print(f"process {proc.pid} =>")
             print(f"P{proc.pid} STARTED")

        # Executa por um quantum ou até terminar o processo
        quantum = proc.quantum
        tempo_nesta_rodada = min(proc.tempo_restante, quantum)
        
        instrucao_inicial = proc.tempo_execucao - proc.tempo_restante + 1
        instrucao_final = instrucao_inicial + tempo_nesta_rodada
        
        print(f"process {proc.pid} =>")
        for i in range(instrucao_inicial, instrucao_final):
            print(f"P{proc.pid} instruction {i}")
            if self.sistema_arquivos:
                self._executar_operacoes_io(proc)
        
        # Atualiza estado
        proc.tempo_restante -= tempo_nesta_rodada
        self._incrementar_espera_outros(tempo_nesta_rodada)

        # Se ainda não terminou, rebaixa prioridade e re-entra na fila
        if proc.tempo_restante > 0:
            # Feedback de prioridade
            nova_prio = min(5, proc.prioridade + 1)
            proc.atualizar_prioridade(nova_prio)
            self.filas_usuario[nova_prio].append(proc) # Volta pra fila
        else:
            print(f"P{proc.pid} return SIGINT")
            # Se acabou, libera tudo
            if proc.recursos_alocados:
                self.gerenciador_recursos.liberar(proc)
            self.gerenciador_memoria.desalocar(proc)

    # Incrementa o tempo de espera de todos os outros processos na fila para aging
    def _incrementar_espera_outros(self, tempo):
        for prio in range(1, 6):
            for proc in self.filas_usuario[prio]:
                proc.tempo_espera += tempo

    # Aplica aging promovendo processos que esperaram demais
    def aplicar_aging(self):
        for prio in range(2, 6):
            promovidos = []
            for proc in self.filas_usuario[prio]:
                if proc.tempo_espera >= self.tempo_limite_aging:
                    promovidos.append(proc)
            
            for proc in promovidos:
                self.filas_usuario[prio].remove(proc)
                nova_prio = prio - 1
                proc.atualizar_prioridade(nova_prio)
                proc.tempo_espera = 0
                self.filas_usuario[nova_prio].append(proc)
                print(f"[AGING] Processo {proc.pid} promovido: Prio {prio} -> {nova_prio}")

    # Verifica se ainda há processos para executar
    def _existem_processos(self):
        if self.fila_global or self.fila_rt: return True
        for fila in self.filas_usuario.values():
            if fila: return True
        return False

    def _executar_operacoes_io(self, processo):
        """Executa operações de I/O do processo"""
        for operacao in processo.operacoes_io:
            if operacao[0] == 'criar':
                _, nome, tamanho = operacao
                self.sistema_arquivos.criar_arquivo(processo, nome, tamanho)
            elif operacao[0] == 'deletar':
                _, nome = operacao
                self.sistema_arquivos.deletar_arquivo(processo, nome)
