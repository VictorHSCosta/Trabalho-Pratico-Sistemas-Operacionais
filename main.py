from classes.processo import Processo
from classes.escalonador import Escalonador
from classes.gerenciador_recursos import GerenciadorRecursos
from classes.sistema_arquivos import SistemaArquivos

if __name__ == "__main__":
    # Inicializa os gerenciadores
    gr = GerenciadorRecursos()
    fs = SistemaArquivos(total_blocos=64)
    
    # Inicializa o disco com alguns arquivos pré-existentes
    fs.inicializar_disco([
        ('sistema.txt', 0, 10),
        ('dados.txt', 20, 15)
    ])
    
    escalonador = Escalonador(gerenciador_recursos=gr, sistema_arquivos=fs)

    # Criando processos de exemplo
    p1 = Processo(
        pid=1, 
        tipo='RT', 
        prioridade=0, 
        tempo_execucao=10, 
        blocos_memoria=10,
        operacoes_io=[
            ('criar', 'rt_file.txt', 5),
            ('deletar', 'dados.txt')
        ]
    )
    
    p2 = Processo(
        pid=2, 
        tipo='USER', 
        prioridade=1, 
        tempo_execucao=10, 
        blocos_memoria=200,
        recursos_necessarios=['SCANNER', 'IMPRESSORA'],
        operacoes_io=[
            ('criar', 'user_doc.txt', 8),
        ]
    )
    
    p3 = Processo(
        pid=3, 
        tipo='USER', 
        prioridade=3, 
        tempo_execucao=4, 
        blocos_memoria=50,
        recursos_necessarios=['MODEM'],
        operacoes_io=[
            ('criar', 'relatorio.txt', 10),
        ]
    )
    
    p4 = Processo(
        pid=4, 
        tipo='USER', 
        prioridade=5, 
        tempo_execucao=20, 
        blocos_memoria=700,
        recursos_necessarios=['SATA'],
        operacoes_io=[
            ('criar', 'backup.txt', 12),
        ]
    )

    escalonador.adicionar_processo(p1)
    escalonador.adicionar_processo(p2)
    escalonador.adicionar_processo(p3)
    escalonador.adicionar_processo(p4)

    escalonador.executar()
    
    # Mostra o mapa final do disco
    fs.imprimir_mapa()
