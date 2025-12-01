import re
from pathlib import Path


def split_campos(linha):
    """Divide uma linha em campos, ignorando separadores comuns. Retorna uma lista desses valores individuais"""
    return [campo for campo in re.split(r"[\s,;]+", linha.strip()) if campo]

#alteracao feita pra deixar claro que args é uma lista
def resolver_caminhos(args : list, base):
    """Resolve caminhos de entrada a partir dos argumentos ou usa o padrão em entradas/.
       Retorna uma tupla (caminho_processos, caminho_arquivos)."""
    if len(args) >= 2:
        return Path(args[0]), Path(args[1])

    return base / "entradas" / "processes.txt", base / "entradas" / "files.txt"


def carregar_processos(caminho):
    """Lê o arquivo de processos e devolve lista ordenada por tempo de início.
       Retorna uma lista de objetos Processo."""
    processos = []

    from classes.processo import Processo  # import local para evitar ciclos

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            if not linha.strip():
                continue

            campos = split_campos(linha)
            if len(campos) != 8:
                raise ValueError(f"Linha invalida em {caminho}: {linha.strip()}")

            inicio, prioridade, tempo_cpu, blocos, impressora, scanner, modem, sata = map(int, campos)
            tipo = "RT" if prioridade == 0 else "USER"

            recursos = []
            if scanner:
                recursos.append("SCANNER")
            if impressora:
                recursos.append("IMPRESSORA")
            if modem:
                recursos.append("MODEM")
            if sata:
                recursos.append("SATA")

            pid = len(processos)
            processo = Processo(
                pid=pid,
                tipo=tipo,
                prioridade=prioridade,
                tempo_execucao=tempo_cpu,
                blocos_memoria=blocos,
                recursos_necessarios=recursos,
                tempo_inicio=inicio,
            )

            processo.usa_scanner = bool(scanner)
            processo.usa_impressora = int(impressora)
            processo.usa_modem = bool(modem)
            processo.usa_sata = int(sata)

            processos.append(processo)
    return processos


def carregar_operacoes_disco(caminho):
    """Lê o arquivo de operações do disco e devolve (total_blocos, arquivos_iniciais, operacoes).
       Retorna uma tupla com o total de blocos, uma lista de arquivos iniciais e uma lista de operações."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    if len(linhas) < 2:
        raise ValueError("Arquivo de operacoes invalido: faltam configuracoes iniciais.")

    total_blocos = int(split_campos(linhas[0])[0])
    segmentos = int(split_campos(linhas[1])[0])

    arquivos_iniciais = []
    indice = 2
    for _ in range(segmentos):
        campos = split_campos(linhas[indice])
        indice += 1
        if len(campos) < 3:
            raise ValueError("Linha de segmento invalida no arquivo de disco.")
        nome, inicio, tamanho = campos[0], int(campos[1]), int(campos[2])
        arquivos_iniciais.append((nome, inicio, tamanho))

    operacoes = []
    for linha in linhas[indice:]:
        campos = split_campos(linha)
        if len(campos) < 3:
            continue
        pid = int(campos[0])
        codigo = int(campos[1])
        nome = campos[2]
        tamanho = int(campos[3]) if codigo == 0 and len(campos) > 3 else None
        operacoes.append((pid, codigo, nome, tamanho))

    return total_blocos, arquivos_iniciais, operacoes
