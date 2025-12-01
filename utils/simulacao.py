from utils.saida import imprimir_despacho, formatar_blocos
from classes.escalonador import Escalonador

escalonador = Escalonador()

def simular_processos(processos, gerenciador_memoria, gerenciador_recursos):
    # Inicializa o escalonador passando as dependências
    escalonador = Escalonador(
        gerenciador_recursos=gerenciador_recursos,
        gerenciador_memoria=gerenciador_memoria
    ) # O sistema de arquivos é passado na main ou ajustado aqui se necessário

    # Ordena por chegada e adiciona TODOS à fila global
    processos.sort(key=lambda x: x.tempo_inicio)
    for processo in processos:
        escalonador.adicionar_processo(processo)
    
    # O Escalonador assume o controle total da simulação
    escalonador.executar()


def executar_operacoes_sistema_arquivos(fs, operacoes, processos):
    """Executa operações do sistema de arquivos segundo a lista fornecida."""
    print("Sistema de arquivos =>")
    processos_por_pid = {proc.pid: proc for proc in processos}

    for indice, operacao in enumerate(operacoes, start=1):
        pid, codigo, nome, tamanho = operacao
        processo = processos_por_pid.get(pid)

        if processo is None:
            print(f"Operacao {indice} => Falha")
            print(f"O processo {pid} nao existe.")
            continue

        if codigo == 0:
            sucesso = fs.criar_arquivo(processo, nome, tamanho or 0, verbose=False)
            info = fs.ultimo_resultado or {}
            if sucesso:
                inicio = info.get("inicio", 0)
                tam = info.get("tamanho", tamanho or 0)
                blocos_desc = formatar_blocos(inicio, tam)
                print(f"Operacao {indice} => Sucesso")
                print(f"O processo {pid} criou o arquivo {nome} ({blocos_desc}).")
            else:
                motivo = info.get("motivo")
                if motivo == "arquivo_existente":
                    mensagem = f"O arquivo {nome} ja existe."
                elif motivo == "sem_espaco":
                    mensagem = f"O processo {pid} nao pode criar o arquivo {nome} (falta de espaco)."
                else:
                    mensagem = f"O processo {pid} nao pode criar o arquivo {nome}."
                print(f"Operacao {indice} => Falha")
                print(mensagem)
        elif codigo == 1:
            sucesso = fs.deletar_arquivo(processo, nome, verbose=False)
            info = fs.ultimo_resultado or {}
            if sucesso:
                print(f"Operacao {indice} => Sucesso")
                print(f"O processo {pid} deletou o arquivo {nome}.")
            else:
                motivo = info.get("motivo")
                if motivo == "inexistente":
                    mensagem = f"O processo {pid} nao pode deletar o arquivo {nome} porque ele nao existe."
                elif motivo == "permissao":
                    mensagem = f"O processo {pid} nao pode deletar o arquivo {nome} (permissao insuficiente)."
                else:
                    mensagem = f"O processo {pid} nao pode deletar o arquivo {nome}."
                print(f"Operacao {indice} => Falha")
                print(mensagem)
        else:
            print(f"Operacao {indice} => Falha")
            print(f"Codigo de operacao {codigo} desconhecido.")

    print("Mapa de ocupacao do disco:")
    print(" ".join(fs.mapa_ocupacao()))

