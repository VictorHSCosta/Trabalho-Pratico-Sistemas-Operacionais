def imprimir_despacho(processo):
    """Mostra informações do processo despachado."""
    print("dispatcher =>")
    print(f" PID: {processo.pid}")
    print(f" offset: {processo.offset if processo.offset is not None else -1}")
    print(f" blocks: {processo.blocos_memoria}")
    print(f" priority: {processo.prioridade}")
    print(f" time: {processo.tempo_execucao}")
    print(f" scanners: {int(bool(processo.usa_scanner))}")
    print(f" printers: {int(bool(processo.usa_impressora))}")
    print(f" modems: {int(bool(processo.usa_modem))}")
    print(f" sata: {int(bool(processo.usa_sata))}")


def formatar_blocos(inicio, tamanho):
    blocos = [str(inicio + desloc) for desloc in range(tamanho)]
    if not blocos:
        return ""
    if len(blocos) == 1:
        return f"bloco {blocos[0]}"
    return "blocos " + ", ".join(blocos[:-1]) + f" e {blocos[-1]}"

