import unittest
import sys
import os

# Add the parent directory to sys.path to allow imports from classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.processo import Processo
from classes.gerenciador_recursos import GerenciadorRecursos

class TestGerenciadorRecursos(unittest.TestCase):
    def setUp(self):
        self.gr = GerenciadorRecursos()

    def test_alocacao_sucesso(self):
        p = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100, 
                     recursos_necessarios=['SCANNER', 'IMPRESSORA'])
        sucesso = self.gr.alocar(p)
        self.assertTrue(sucesso)
        self.assertEqual(self.gr.recursos['SCANNER'], 0)
        self.assertEqual(self.gr.recursos['IMPRESSORA'], 1)

    def test_alocacao_falha_sem_recurso(self):
        # Ocupa o scanner
        p1 = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100,
                      recursos_necessarios=['SCANNER'])
        self.gr.alocar(p1)
        
        # Tenta alocar outro scanner
        p2 = Processo(pid=2, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100,
                      recursos_necessarios=['SCANNER'])
        sucesso = self.gr.alocar(p2)
        self.assertFalse(sucesso)

    def test_liberacao(self):
        p = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100,
                     recursos_necessarios=['SCANNER', 'MODEM'])
        self.gr.alocar(p)
        self.assertEqual(self.gr.recursos['SCANNER'], 0)
        self.assertEqual(self.gr.recursos['MODEM'], 0)
        
        self.gr.liberar(p)
        self.assertEqual(self.gr.recursos['SCANNER'], 1)
        self.assertEqual(self.gr.recursos['MODEM'], 1)

    def test_multiplos_recursos_mesmo_tipo(self):
        p = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100,
                     recursos_necessarios=['IMPRESSORA', 'IMPRESSORA'])
        sucesso = self.gr.alocar(p)
        self.assertTrue(sucesso)
        self.assertEqual(self.gr.recursos['IMPRESSORA'], 0)

    def test_rt_nao_precisa_recursos(self):
        p = Processo(pid=1, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=50)
        sucesso = self.gr.alocar(p)
        self.assertTrue(sucesso) # RT não precisa de recursos

if __name__ == '__main__':
    unittest.main()
