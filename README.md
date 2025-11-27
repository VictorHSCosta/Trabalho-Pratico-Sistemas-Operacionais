# Trabalho Prático – Sistemas Operacionais

Repositório do trabalho prático da disciplina de Sistemas Operacionais. Os scripts principais estão no diretório raiz (`main.py` e `escalonador.py`) e os testes automatizados ficam no diretório `tests/`.

## Pré-requisitos

- Python 3.10 ou superior instalado
- `pip` atualizado (`python -m pip install --upgrade pip`)

## Preparando o ambiente virtual

1. Crie o ambiente virtual: `python -m venv .venv`
2. Ative o ambiente
   - Linux/macOS: `source .venv/bin/activate`
   - Windows (PowerShell): `.\.venv\Scripts\Activate.ps1`
3. Instale as dependências (caso exista `requirements.txt`): `pip install -r requirements.txt`

Quando terminar de trabalhar, desative o ambiente com `deactivate`.

## Executando os testes

Com o ambiente virtual ativo na raiz do projeto:

```
python -m unittest discover -s tests -v
```

## Executando a aplicação principal

Ainda na raiz do projeto e com o ambiente ativo:

```
python main.py
```

O script `main.py` é responsável por instanciar o escalonador e rodar os experimentos definidos no trabalho.
