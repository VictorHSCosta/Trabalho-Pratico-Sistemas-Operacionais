import sys
from pathlib import Path

from classes.gerenciador_memoria import GerenciadorMemoria
from classes.gerenciador_recursos import GerenciadorRecursos
from classes.sistema_arquivos import SistemaArquivos
from utils.entrada import carregar_operacoes_disco, carregar_processos, resolver_caminhos
from utils.simulacao import executar_operacoes_sistema_arquivos, simular_processos


def main():
    base = Path(__file__).parent
    processos_path, arquivos_path = resolver_caminhos(sys.argv[1:], base)

    if not processos_path.exists() or not arquivos_path.exists():
        print("Arquivos de entrada nao encontrados.")
        print(f"Esperado: {processos_path} e {arquivos_path}")
        sys.exit(1)

    processos = carregar_processos(processos_path)
    total_blocos, arquivos_iniciais, operacoes = carregar_operacoes_disco(arquivos_path)

    gerenciador_memoria = GerenciadorMemoria()
    gerenciador_recursos = GerenciadorRecursos()
    sistema_arquivos = SistemaArquivos(total_blocos=total_blocos)
    sistema_arquivos.inicializar_disco(arquivos_iniciais)

    simular_processos(processos, gerenciador_memoria, gerenciador_recursos)
    executar_operacoes_sistema_arquivos(sistema_arquivos, operacoes, processos)


if __name__ == "__main__":
    main()
