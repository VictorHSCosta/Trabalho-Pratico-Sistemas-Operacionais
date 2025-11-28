import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.gerenciador_memoria import GerenciadorMemoria
from classes.gerenciador_recursos import GerenciadorRecursos
from classes.processo import Processo
from classes.sistema_arquivos import SistemaArquivos
from utils.entrada import carregar_operacoes_disco, carregar_processos, resolver_caminhos, split_campos
from utils.saida import formatar_blocos
from utils.simulacao import executar_operacoes_sistema_arquivos, simular_processos


class TestUtilsEntrada(unittest.TestCase):
    def test_split_campos(self):
        campos = split_campos("1, 2; 3  4")
        self.assertEqual(campos, ["1", "2", "3", "4"])

    def test_resolver_caminhos_args(self):
        base = Path("/tmp/base")
        p1, p2 = resolver_caminhos(["a.txt", "b.txt"], base)
        self.assertEqual(p1, Path("a.txt"))
        self.assertEqual(p2, Path("b.txt"))

    def test_carregar_processos(self):
        conteudo = """2, 0, 3, 10, 1, 1, 0, 0
1, 1, 1, 5, 0, 0, 1, 1
"""
        with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
            tmp.write(conteudo)
            tmp_path = Path(tmp.name)

        processos = carregar_processos(tmp_path)

        self.assertEqual([p.pid for p in processos], [0, 1])
        self.assertEqual([p.tempo_inicio for p in processos], [2, 1])
        self.assertTrue(processos[0].usa_scanner)
        self.assertEqual(processos[0].usa_impressora, 1)
        self.assertTrue(processos[1].usa_modem)
        self.assertEqual(processos[1].usa_sata, 1)

        tmp_path.unlink()

    def test_carregar_operacoes_disco(self):
        conteudo = """10
2
A, 0, 1
B, 1, 2
0, 0, C, 3
1, 1, A
"""
        with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
            tmp.write(conteudo)
            tmp_path = Path(tmp.name)

        total, iniciais, ops = carregar_operacoes_disco(tmp_path)

        self.assertEqual(total, 10)
        self.assertEqual(iniciais, [("A", 0, 1), ("B", 1, 2)])
        self.assertEqual(ops, [(0, 0, "C", 3), (1, 1, "A", None)])

        tmp_path.unlink()


class TestUtilsSaida(unittest.TestCase):
    def test_formatar_blocos(self):
        self.assertEqual(formatar_blocos(0, 1), "bloco 0")
        self.assertEqual(formatar_blocos(2, 3), "blocos 2, 3 e 4")


class TestUtilsSimulacao(unittest.TestCase):
    def test_simular_processos_output(self):
        gm = GerenciadorMemoria()
        gr = GerenciadorRecursos()
        processos = [Processo(pid=0, tipo="RT", prioridade=0, tempo_execucao=2, blocos_memoria=2)]

        buf = io.StringIO()
        with redirect_stdout(buf):
            simular_processos(processos, gm, gr)

        saida = buf.getvalue()
        self.assertIn("dispatcher =>", saida)
        self.assertIn("P0 STARTED", saida)
        self.assertIn("P0 instruction 2", saida)

    def test_executar_operacoes_sistema_arquivos(self):
        fs = SistemaArquivos(total_blocos=10)
        fs.inicializar_disco([("X", 0, 2)])
        processos = [Processo(pid=0, tipo="RT", prioridade=0, tempo_execucao=1, blocos_memoria=1)]
        operacoes = [(0, 0, "A", 3), (0, 1, "X", None)]

        buf = io.StringIO()
        with redirect_stdout(buf):
            executar_operacoes_sistema_arquivos(fs, operacoes, processos)

        saida = buf.getvalue()
        self.assertIn("Operacao 1 => Sucesso", saida)
        self.assertIn("Operacao 2 => Sucesso", saida)
        self.assertIn("Mapa de ocupacao do disco:", saida)


if __name__ == "__main__":
    unittest.main()
