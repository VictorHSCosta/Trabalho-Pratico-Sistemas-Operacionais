import unittest
import sys
import os

# Add the parent directory to sys.path to allow imports from classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.processo import Processo

class TestProcesso(unittest.TestCase):
    def test_inicializacao_rt(self):
        p = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=50)
        self.assertEqual(p.pid, 1)
        self.assertEqual(p.tipo, 'RT')
        self.assertEqual(p.prioridade, 0)
        self.assertEqual(p.tempo_execucao, 10)
        self.assertEqual(p.blocos_memoria, 50)
        self.assertEqual(p.tempo_restante, 10)
        self.assertEqual(p.quantum, 0)

    def test_inicializacao_user(self):
        p = Processo(pid=2, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        self.assertEqual(p.pid, 2)
        self.assertEqual(p.tipo, 'USER')
        self.assertEqual(p.prioridade, 1)
        self.assertEqual(p.quantum, 6) # Prio 1 -> Quantum 6

    def test_atualizar_prioridade(self):
        p = Processo(pid=2, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        p.atualizar_prioridade(2)
        self.assertEqual(p.prioridade, 2)
        self.assertEqual(p.quantum, 5) # Prio 2 -> Quantum 5

    def test_atualizar_prioridade_rt_ignora(self):
        p = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=50)
        p.atualizar_prioridade(2)
        self.assertEqual(p.prioridade, 0) # Não deve mudar
        self.assertEqual(p.quantum, 0)

if __name__ == '__main__':
    unittest.main()
