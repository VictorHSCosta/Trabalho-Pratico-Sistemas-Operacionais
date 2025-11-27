import unittest
import sys
import os

# Add the parent directory to sys.path to allow imports from classes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from classes.processo import Processo
from classes.sistema_arquivos import SistemaArquivos

class TestSistemaArquivos(unittest.TestCase):
    def setUp(self):
        self.fs = SistemaArquivos(total_blocos=100)

    def test_criar_arquivo_sucesso(self):
        p = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        sucesso = self.fs.criar_arquivo(p, 'teste.txt', 10)
        self.assertTrue(sucesso)
        self.assertIn('teste.txt', self.fs.arquivos)
        self.assertEqual(self.fs.arquivos['teste.txt']['criador'], 1)

    def test_criar_arquivo_duplicado(self):
        p = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        self.fs.criar_arquivo(p, 'teste.txt', 10)
        sucesso = self.fs.criar_arquivo(p, 'teste.txt', 5)
        self.assertFalse(sucesso)

    def test_criar_arquivo_sem_espaco(self):
        p = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        # Ocupa todo o disco
        self.fs.criar_arquivo(p, 'grande.txt', 100)
        # Tenta criar outro
        sucesso = self.fs.criar_arquivo(p, 'pequeno.txt', 1)
        self.assertFalse(sucesso)

    def test_deletar_arquivo_proprio(self):
        p = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        self.fs.criar_arquivo(p, 'meu.txt', 10)
        sucesso = self.fs.deletar_arquivo(p, 'meu.txt')
        self.assertTrue(sucesso)
        self.assertNotIn('meu.txt', self.fs.arquivos)

    def test_deletar_arquivo_alheio_user(self):
        p1 = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        p2 = Processo(pid=2, tipo='USER', prioridade=2, tempo_execucao=10, blocos_memoria=100)
        
        self.fs.criar_arquivo(p1, 'arquivo_p1.txt', 10)
        sucesso = self.fs.deletar_arquivo(p2, 'arquivo_p1.txt')
        self.assertFalse(sucesso)
        self.assertIn('arquivo_p1.txt', self.fs.arquivos)

    def test_deletar_arquivo_rt_pode_tudo(self):
        p_user = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        p_rt = Processo(pid=2, tipo='RT', prioridade=0, tempo_execucao=10, blocos_memoria=50)
        
        self.fs.criar_arquivo(p_user, 'user_file.txt', 10)
        sucesso = self.fs.deletar_arquivo(p_rt, 'user_file.txt')
        self.assertTrue(sucesso)
        self.assertNotIn('user_file.txt', self.fs.arquivos)

    def test_first_fit(self):
        p = Processo(pid=1, tipo='USER', prioridade=1, tempo_execucao=10, blocos_memoria=100)
        
        # Cria arquivo1 (blocos 0-9)
        self.fs.criar_arquivo(p, 'arq1.txt', 10)
        # Cria arquivo2 (blocos 10-19)
        self.fs.criar_arquivo(p, 'arq2.txt', 10)
        # Deleta arquivo1 (libera 0-9)
        self.fs.deletar_arquivo(p, 'arq1.txt')
        # Cria arquivo3 de tamanho 5 (deve ir para 0-4, first-fit)
        self.fs.criar_arquivo(p, 'arq3.txt', 5)
        
        self.assertEqual(self.fs.arquivos['arq3.txt']['inicio'], 0)

if __name__ == '__main__':
    unittest.main()
