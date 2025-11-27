import time
from collections import deque

class Escalonador:
    def __init__(self):
        self.fila_global = deque() # Fila de entrada
        self.fila_rt = deque()     # Fila Tempo Real (Prio 0)
        self.filas_usuario = {
            1: deque(),
            2: deque(),
            3: deque(),
            4: deque(),
            5: deque()
        }
        self.tempo_limite_aging = 10  # Ciclos de espera para promover processo
        self.max_processos = 100

    def adicionar_processo(self, processo):
        if len(self.fila_global) + self._total_processos_ativos() < self.max_processos:
            self.fila_global.append(processo)
            print(f"Processo {processo.pid} adicionado à Fila Global.")
        else:
            print(f"Erro: Capacidade máxima de processos ({self.max_processos}) atingida.")

    def _total_processos_ativos(self):
        count = len(self.fila_rt)
        for fila in self.filas_usuario.values():
            count += len(fila)
        return count

    def distribuir_processos(self):
        """Move processos da fila global para suas filas específicas"""
        while self.fila_global:
            proc = self.fila_global.popleft()
            if proc.tipo == 'RT':
                self.fila_rt.append(proc)
                print(f"Processo {proc.pid} movido para Fila Tempo Real.")
            else:
                # Garante que prioridade esteja entre 1 e 5
                prio = max(1, min(5, proc.prioridade))
                proc.atualizar_prioridade(prio)
                self.filas_usuario[prio].append(proc)
                print(f"Processo {proc.pid} movido para Fila Usuário (Prio {prio}).")

    def executar(self):
        print("\n--- Iniciando Execução do Escalonador ---\n")
        
        while self._existem_processos():
            self.distribuir_processos()
            self.aplicar_aging()

            # 1. Tenta executar Tempo Real (Precedência Absoluta)
            if self.fila_rt:
                self._executar_rt()
                continue # Volta ao início para verificar se novos processos chegaram (simulação)

            # 2. Tenta executar Processos de Usuário (Maior prioridade primeiro)
            executou_usuario = False
            for prio in range(1, 6):
                if self.filas_usuario[prio]:
                    self._executar_usuario(prio)
                    executou_usuario = True
                    break
            
            if not executou_usuario and not self.fila_rt:
                print("Ocioso...")
                time.sleep(0.5)

        print("\n--- Todos os processos finalizados ---")

    def _executar_rt(self):
        proc = self.fila_rt[0] # FIFO: olha o primeiro sem remover ainda
        print(f"> Executando RT {proc.pid} (Não-preemptivo)...")
        
        # Simula execução completa
        tempo_gasto = proc.tempo_restante
        time.sleep(1) # Simulação visual
        proc.tempo_restante = 0
        
        print(f"  Processo RT {proc.pid} finalizado.")
        self.fila_rt.popleft() # Remove após terminar
        self._incrementar_espera_outros(tempo_gasto)

    def _executar_usuario(self, prio_atual):
        fila = self.filas_usuario[prio_atual]
        proc = fila.popleft()
        
        quantum = proc.quantum
        tempo_exec = min(proc.tempo_restante, quantum)
        
        print(f"> Executando Usuário {proc.pid} (Prio {proc.prioridade}) por {tempo_exec}s...")
        time.sleep(0.5) # Simulação visual
        
        proc.tempo_restante -= tempo_exec
        self._incrementar_espera_outros(tempo_exec)

        if proc.tempo_restante > 0:
            # Feedback: Reduz prioridade (aumenta valor numérico)
            nova_prio = min(5, proc.prioridade + 1)
            if nova_prio != proc.prioridade:
                print(f"  Processo {proc.pid} sofreu preempção. Prioridade {proc.prioridade} -> {nova_prio}")
                proc.atualizar_prioridade(nova_prio)
            else:
                print(f"  Processo {proc.pid} sofreu preempção. Mantém prioridade {proc.prioridade}.")
            
            self.filas_usuario[nova_prio].append(proc)
        else:
            print(f"  Processo Usuário {proc.pid} finalizado.")

    def _incrementar_espera_outros(self, tempo):
        """Incrementa tempo de espera para todos os processos nas filas de usuário"""
        for prio in range(1, 6):
            for proc in self.filas_usuario[prio]:
                proc.tempo_espera += tempo

    def aplicar_aging(self):
        """Verifica starvation e promove processos"""
        for prio in range(2, 6): # Começa da prioridade 2, pois 1 já é a maior de usuário
            # Precisamos iterar com cuidado pois vamos modificar as filas
            processos_para_promover = []
            
            for proc in self.filas_usuario[prio]:
                if proc.tempo_espera >= self.tempo_limite_aging:
                    processos_para_promover.append(proc)
            
            for proc in processos_para_promover:
                self.filas_usuario[prio].remove(proc)
                nova_prio = prio - 1
                proc.atualizar_prioridade(nova_prio)
                proc.tempo_espera = 0 # Reseta espera após promoção
                self.filas_usuario[nova_prio].append(proc)
                print(f"[AGING] Processo {proc.pid} promovido: Prio {prio} -> {nova_prio}")

    def _existem_processos(self):
        if self.fila_global or self.fila_rt:
            return True
        for fila in self.filas_usuario.values():
            if fila:
                return True
        return False
