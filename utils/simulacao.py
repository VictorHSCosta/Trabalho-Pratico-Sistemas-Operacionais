from utils.saida import imprimir_despacho, formatar_blocos


def simular_processos(processos, gerenciador_memoria, gerenciador_recursos):
    """Executa alocação, simulação de instruções e liberação de cada processo."""
    for processo in processos:
        alocou_memoria = gerenciador_memoria.alocar(processo)
        imprimir_despacho(processo)

        if not alocou_memoria:
            print(f"process {processo.pid} =>")
            print(f"P{processo.pid} NAO INICIADO (sem memoria)")
            continue

        recursos_ok = gerenciador_recursos.alocar(processo)
        if not recursos_ok:
            print(f"process {processo.pid} =>")
            print(f"P{processo.pid} NAO INICIADO (recursos indisponiveis)")
            gerenciador_memoria.desalocar(processo)
            continue

        print(f"process {processo.pid} =>")
        print(f"P{processo.pid} STARTED")
        for instrucao in range(1, processo.tempo_execucao + 1):
            print(f"P{processo.pid} instruction {instrucao}")
        print(f"P{processo.pid} return SIGINT")

        gerenciador_recursos.liberar(processo)
        gerenciador_memoria.desalocar(processo)


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

