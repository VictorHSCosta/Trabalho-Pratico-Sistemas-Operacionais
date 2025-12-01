## Sobre as entradas vamos ter:

### Iremos ter um arquivo cheio de linhas, e cada linha vai representar um processo aonde cada número vai significar:

```bash 
<tempo de inicializacão> 
<prioridade> 
<tempo de processador> 
<blocos em memória> 
<número código da impressora requisitada> 
<requisicão do scanner> 
<requisicão do modem> 
<número código do disco>
```

### Também teremos outro que vai funcionar da seguinte forma:

```bash
<quantidade total de blocos no disco>
<quantidade de segmentos ocupados>
<identificacão de quais arquivos já estão gravados no disco>
<localizacão dos blocos usados por cada arquivo>
<identificacão de qual processo efetuará cada operacão>
<identificacão das operacões (código 0 = criar arquivo e código 1 = deletar arquivo)>
```

Para as operacões de criacão um nome de arquivo deve ser constado e a quantidade de blocos ocupados pelo arquivo também. Na de deletar somente o nome do arquivo a ser deletado deve ser constada.

A organizacão será:

- Linha 1: Quantidade de blocos do disco
- Linha 2: Quantidade de segmentos ocupados no disco (n)
- Linha 3 até linha n + 2: Arquivo (identificado por uma letra), número do primeiro bloco gravado, quantidade de blocos ocupadas por esse arquivo.
- A partir da linha n + 3: Cada linha representa uma operacão a ser efetivada pelo sistemas de arquivos. Nelas vão conter:

```bash
<ID_Processo> -> Deve sempre iniciar em 0
<Código_Operacão>
<Nome_arquivo>
<se_operacaoCriar_numero_blocos>
```