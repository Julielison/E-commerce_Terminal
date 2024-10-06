# Sistema de E-commerce | Projeto interdisciplinar

<!-- Substitua pelo título do seu projeto, por exemplo: "Sistema de E-commerce com Cliente-Servidor" -->

## Autores
- **Nome:** Julielison Lima
- **E-mail:** lima.julielison@academico.ifpb.edu.br
---
- **Nome:** Filipe Bruzaca
- **E-mail:** filipe.cavalcante@academico.ifpb.edu.br
---
- **Nome:** Flávio Henrique
- **E-mail:** albuquerque.flavio@academico.ifpb.edu.br

## Disciplinas Envolvidas
- **Disciplina 1:** Protocolos de Interconxeção de Redes - Leônidas Lima
- **Disciplina 2:** Estrutura de Dados - Alex Sandro

## Descrição do Problema


O sistema proposto é uma plataforma de e-commerce que permite que clientes visualizem produtos, adicionem itens ao carrinho e realizem compras através de uma comunicação cliente-servidor. A aplicação oferece funcionalidades como consulta de produtos, categorias, e a possibilidade de gerenciar o carrinho de compras.

## Arquivos do Projeto

| Arquivo                | Descrição                                                                 |
|------------------------|---------------------------------------------------------------------------|
| `servidor.py`          | Classe que implementa um servidor TCP multi-thread para processar requisições de clientes e interagir com o estoque de produtos. |
| `cliente.py`            | Arquivo responsável pela interface do cliente e comunicação com o servidor.|
| `protocolo.py`          | Contém a definição das funções e métodos do protocolo de comunicação.     |
| `estoque.py`    | Módulo que gerencia o estoque de produtos disponíveis no servidor.        |
| `protocolo.csv`| Arquivo CSV que contém os métodos e os códigos de sucesso e erro.         |
| `categoria.py` | Classe que representa uma categoria com um nome, gerenciando o armazenamento e o acesso ao nome da categoria. |
| `produto.py` | Classe usada para criar um objeto produto com atributos como nome, preço, quantidade e categoria. Contém métodos para gerenciar e validar os atributos do produto, incluindo nome, preço, quantidade e categoria. |
| `sql.py`                | Classe Sql que contém métodos para retornar consultas SQL utilizadas no sistema de estoque. Os métodos desta classe retornam comandos SQL para buscar produtos e categorias no banco de dados. |
| `LinearProbingLoadFactor.py` | Contém a HashTable usada para guardar os produtos e também os métodos, códigos de erro, sucesso, e funções associadas ao protocolo.
| `listaEncadeada.py` | Contém a lista simplesmente simplesmente encadeada, usada para armazenar os objetos de cada categoria. |

## Estruturas de dados usadas
### Cliente
- HashTable

### Servidor
- HashTable
- Lista simplesmente encadeada

## Pré-requisitos para Execução
- Python versão 3.12.1 ou superior
- Antes de executar a aplicação, certifique-se de ter os seguintes pacotes instalados:

| Pacote/Biblioteca | Propósito                                                                 | Instalação                                                      |
|-------------------|---------------------------------------------------------------------------|-----------------------------------------------------------------|
| `socket`          | Comunicação cliente-servidor via TCP.                                     | Instalado por padrão no Python.                                 |
| `threading`       | Para executar múltiplas threads simultaneamente.                          | Instalado por padrão no Python.                                 |
| `tabulate`        | Utilizado para formatar tabelas de dados no cliente.                      | `pip install tabulate`                                          |
| `numpy`           | Utilizado para criar um array eficiente que guarda os valores da hashtable | `pip install numpy` |

## Protocolo da Aplicação

Aqui está a documentação das mensagens trocadas entre o cliente e o servidor:

### Solicitações do Cliente
| Método           | Parâmetros                     | Descrição                                                        |
|------------------|--------------------------------|------------------------------------------------------------------|
| `PEGAR_PRODUTOS` | Nenhum                         | Retorna uma lista de todos os produtos disponíveis.               |
| `PEGAR_CATEGORIAS`| Nenhum                        | Retorna uma lista de todas as categorias disponíveis.             |
| `COMPRAR`        | `id_produto:quantidade;id_produto:quantidade`  | Envia uma solicitação para finalizar a compra dos produtos no carrinho, podendo ser mais de um produto|
| `SAIR`           | Nenhum                         | Finaliza a sessão do cliente e desconecta do servidor.            |

### Respostas do Servidor
| Código de Resposta | Descrição                                                         | Formatação                           |
|--------------------|-------------------------------------------------------------------|--------------------------------------|
| `PROD-220`         | Indica que a consulta de produtos foi realizada com sucesso e que os dados deles foram retornados.        | PROD-220@#id_produto#nome#preço#quant##id_produto#nome#preço#quant... |
| `CATE-221`         | Indica que a consulta de categorias foi realizada com sucesso, ou seja, os nomes das categorias foram retornados                                        | CATE-221@#c1#c2#c3#c4... |
| `PRCA-222`         | Indica que foram retornados produtos para a categoria especificada .| PQAS-224@#id_produto#nome#preço#quant##id_produto#nome#preço#quant... |
| `COMP-223`         | A compra foi realizada com sucesso, e o pedido foi confirmado.| COMP-223@#Compra_finalizada. |
| `PQAS-224`         | A pesquisa foi realizada com sucesso, e os produtos que contém o nome foram retornados.| PQAS-224@#id_produto#nome#preço#quant##id_produto#nome#preço#quant...|
| `ERRO-305`         | Mensagem de erro genérico para métodos não encontrados ou inválidos.| ERRO-305@#Método não encontrado.|
| `ERRO-304`         | Mensagem de erro devido à inexistência do produto.| ERRO-304@#Nenhum_produto_encontrado. |
| `ERRO-303`         | Mensagem de erro contendo a quantidade do produto existente.| ERRO-303@#Quantidade_ou_produto_indisponível id_produto#nome#preço#quant##id_produto#nome#preço#quant...
| `ERRO-302`         | Devolve esse erro quando não existem produtos para categoria especificada.| ERRO-302@#Sem_produtos_para_essa_categoria. |
| `ERRO-301`         | Sem categorias no estoque | ERRO-301@#Sem_categorias.
| `ERRO-300`         | Indica que não há mais produtos no estoque ou não há mais produtos para serem exibidos (em caso de paginação)| ERRO-300@#Sem_produtos_para_exibir.

## Instruções para Execução

Siga os passos abaixo para executar a aplicação cliente-servidor:

### Linux e Windows
#### 1. Executar o Servidor
No terminal, acesse o diretório do projeto e execute o seguinte comando para iniciar o servidor:

`python ./Servidor/servidor.py`

Após isso, o servidor será aberto

#### 2. Executar o Cliente

`python ./Cliente/cliente.py`


Após isso, o cliente será  aberto e será conectado ao servidor

#### 3. Execução do codigo

Irá aparecer uma mensagem de boas vindas e perguntará o nome do usuario

`Bem-vindo ao E-commerce! Por favor, insira seu nome:`

Após digitar o nome do usuario, aparecerá um menu onde digitando de 1-5 poderá ter acesso as funcionalidades do programa, assim como no menu abaixo

`Olá, fulano! Abaixo estão as opções disponíveis:`

        [1] VER PRODUTOS
        [2] VER CATEGORIAS
        [3] ADICIONAR PRODUTO AO CARRINHO
        [4] FINALIZAR COMPRA
        [5] SAIR
        

`Escolha uma opção:`

Dessa forma, ao digitar:

1: O usuário poderá visualizar os produtos disponíveis para compra.

2: O usuário verá exemplos de categorias de produtos.

3: O usuário poderá adicionar produtos ao carrinho de compras pelo seu ID e também poderá especificar a quantidade desejada.

4: O usuário será levado ao carrinho de compras, onde poderá revisar os produtos selecionados e finalizar a compra.

5: A aplicação será fechada.





