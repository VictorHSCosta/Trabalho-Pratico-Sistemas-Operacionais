from classes.processo import Processo
from classes.escalonador import Escalonador

if __name__ == "__main__":
    escalonador = Escalonador()

    # Criando processos de exemplo
    p1 = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=10)
    p2 = Processo(pid=2, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=200) # Deve rodar 6s, sobrar 4s, cair pra Prio 2
    p3 = Processo(pid=3, tipo='USER', prioridade=3, tempo_execucao=4, blocos_memoria=50)
    p4 = Processo(pid=4, tipo='USER', prioridade=5, tempo_execucao=20, blocos_memoria=700) # Vai sofrer aging eventualmente

    escalonador.adicionar_processo(p1)
    escalonador.adicionar_processo(p2)
    escalonador.adicionar_processo(p3)
    escalonador.adicionar_processo(p4)

    escalonador.executar()
