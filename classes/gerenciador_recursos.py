from collections import deque

class GerenciadorRecursos:
    def __init__(self):
        # Capacidade física inicial de cada recurso (valor do semáforo contável)
        self.capacidade = {
            'SCANNER': 1,
            'IMPRESSORA': 2,
            'MODEM': 1,
            'SATA': 3
        }

        # Estado atual dos semáforos (quantidades disponíveis)
        self.recursos = self.capacidade.copy()

        # Mapeia PID -> lista de recursos alocados
        self.alocados = {}

        # Fila FIFO de processos bloqueados por recurso
        self.espera = {
            'SCANNER': deque(),
            'IMPRESSORA': deque(),
            'MODEM': deque(),
            'SATA': deque()
        }

    def P(self, processo, recurso):
        """Semáforo DOWN: tenta adquirir 1 unidade do recurso.
        Decrementa primeiro; se o resultado for < 0 → não há recurso suficiente,
        o processo é bloqueado e colocado na fila de espera."""
        self.recursos[recurso] -= 1

        if self.recursos[recurso] < 0:
            processo.bloqueado = True
            processo.recurso_bloqueio = recurso
            self.espera[recurso].append(processo)
            return False

        return True

    def V(self, recurso):
        """Semáforo UP: libera 1 unidade do recurso.
        Incrementa; se existir processo na fila de espera,
        desbloqueia o primeiro (FIFO) e retorna ele."""
        self.recursos[recurso] += 1

        # há alguém esperando?
        if self.espera[recurso]:
            proc = self.espera[recurso].popleft()
            proc.bloqueado = False
            proc.recurso_bloqueio = None
            return proc

        return None

    def alocar(self, processo):
        """Tenta adquirir todos os recursos necessários (P).
        Se algum falhar, desfaz (V) os recursos já obtidos para evitar alocação parcial."""
        recursos_ok = []

        for rec in processo.recursos_necessarios:
            if self.P(processo, rec):
                recursos_ok.append(rec)
            else:
                for r in recursos_ok:
                    self.V(r)
                return False

        self.alocados[processo.pid] = list(processo.recursos_necessarios)
        return True

    def liberar(self, processo):
        """Libera os recursos alocados por um processo (V).
        Para cada V realizado, pode desbloquear 1 processo.
        Retorna a lista de processos desbloqueados."""
        if processo.pid not in self.alocados:
            return []

        recursos_proc = self.alocados.pop(processo.pid)
        desbloqueados = []

        for rec in recursos_proc:
            p = self.V(rec)
            if p:
                desbloqueados.append(p)

        return desbloqueados
