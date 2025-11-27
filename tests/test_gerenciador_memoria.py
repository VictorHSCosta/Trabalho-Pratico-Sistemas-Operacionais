import unittest
import sys
import os

# Add the parent directory to sys.path to allow imports from classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.processo import Processo
from classes.gerenciador_memoria import GerenciadorMemoria

class TestGerenciadorMemoria(unittest.TestCase):
    def setUp(self):
        self.gm = GerenciadorMemoria()

    def test_alocacao_rt_sucesso(self):
        p = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=10)
        sucesso = self.gm.alocar(p)
        self.assertTrue(sucesso)
        # Verifica se alocou no início (0-9)
        for i in range(10):
            self.assertEqual(self.gm.memoria[i], 1)

    def test_alocacao_rt_falha_sem_espaco(self):
        # Ocupa todos os 64 blocos RT
        p_ocupar = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=64)
        self.gm.alocar(p_ocupar)
        
        p_novo = Processo(pid=2, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=1)
        sucesso = self.gm.alocar(p_novo)
        self.assertFalse(sucesso)

    def test_alocacao_user_sucesso(self):
        p = Processo(pid=2, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        sucesso = self.gm.alocar(p)
        self.assertTrue(sucesso)
        # Verifica se alocou a partir do bloco 64
        for i in range(64, 164):
            self.assertEqual(self.gm.memoria[i], 2)

    def test_alocacao_user_falha_sem_espaco(self):
        # Ocupa todos os 960 blocos User
        p_ocupar = Processo(pid=2, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=960)
        self.gm.alocar(p_ocupar)
        
        p_novo = Processo(pid=3, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=1)
        sucesso = self.gm.alocar(p_novo)
        self.assertFalse(sucesso)

    def test_desalocacao(self):
        p = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=10)
        self.gm.alocar(p)
        self.assertEqual(self.gm.memoria[0], 1)
        
        desalocou = self.gm.desalocar(p)
        self.assertTrue(desalocou)
        self.assertIsNone(self.gm.memoria[0])

    def test_alocacao_contigua(self):
        # Aloca P1 (10 blocos)
        p1 = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=10)
        self.gm.alocar(p1)
        
        # Aloca P2 (10 blocos)
        p2 = Processo(pid=2, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=10)
        self.gm.alocar(p2)
        
        # Desaloca P1 (libera 0-9)
        self.gm.desalocar(p1)
        
        # Tenta alocar P3 (15 blocos) - não deve caber no buraco de 10
        p3 = Processo(pid=3, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=15)
        sucesso = self.gm.alocar(p3)
        self.assertTrue(sucesso)
        
        # Deve ter alocado APÓS P2 (que ocupa 10-19), ou seja, a partir de 20
        # Pois o buraco 0-9 é muito pequeno
        self.assertEqual(self.gm.memoria[20], 3)

if __name__ == '__main__':
    unittest.main()
