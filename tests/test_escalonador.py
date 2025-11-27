import unittest
import sys
import os
from collections import deque

# Add the parent directory to sys.path to allow imports from classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.processo import Processo
from classes.escalonador import Escalonador

class TestEscalonador(unittest.TestCase):
    def setUp(self):
        self.escalonador = Escalonador()

    def test_adicionar_processo(self):
        p = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10)
        self.escalonador.adicionar_processo(p)
        self.assertIn(p, self.escalonador.fila_global)

    def test_distribuir_processos_rt(self):
        p = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10)
        self.escalonador.adicionar_processo(p)
        self.escalonador.distribuir_processos()
        self.assertIn(p, self.escalonador.fila_rt)
        self.assertNotIn(p, self.escalonador.fila_global)

    def test_distribuir_processos_user(self):
        p = Processo(pid=2, tipo='USER', prioridade=1, tempo_execucao=10)
        self.escalonador.adicionar_processo(p)
        self.escalonador.distribuir_processos()
        self.assertIn(p, self.escalonador.filas_usuario[1])
        self.assertNotIn(p, self.escalonador.fila_global)

    def test_aging(self):
        # Configura aging para teste rápido
        self.escalonador.tempo_limite_aging = 5
        p = Processo(pid=3, tipo='USER', prioridade=2, tempo_execucao=10)
        p.tempo_espera = 5 # Simula espera
        
        self.escalonador.filas_usuario[2].append(p)
        self.escalonador.aplicar_aging()
        
        # Deve ter sido movido para prio 1
        self.assertNotIn(p, self.escalonador.filas_usuario[2])
        self.assertIn(p, self.escalonador.filas_usuario[1])
        self.assertEqual(p.prioridade, 1)
        self.assertEqual(p.tempo_espera, 0)

if __name__ == '__main__':
    unittest.main()
