# Sistema de E-commerce

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

## Pré-requisitos para Execução

Antes de executar a aplicação, certifique-se de ter os seguintes pacotes instalados:

| Pacote/Biblioteca | Propósito                                                                 | Instalação                                                      |
|-------------------|---------------------------------------------------------------------------|-----------------------------------------------------------------|
| `socket`          | Comunicação cliente-servidor via TCP.                                     | Instalado por padrão no Python.                                 |
| `threading`       | Para executar múltiplas threads simultaneamente.                          | Instalado por padrão no Python.                                 |
| `tabulate`        | Utilizado para formatar tabelas de dados no cliente.                      | `pip install tabulate`                                          |

## Protocolo da Aplicação

Aqui está a documentação das mensagens trocadas entre o cliente e o servidor:

### Solicitações do Cliente
| Método           | Parâmetros                     | Descrição                                                        |
|------------------|--------------------------------|------------------------------------------------------------------|
| `PEGAR_PRODUTOS` | Nenhum                         | Retorna uma lista de todos os produtos disponíveis.               |
| `PEGAR_CATEGORIAS`| Nenhum                        | Retorna uma lista de todas as categorias disponíveis.             |
| `COMPRAR`        | `ID:quantidade;ID:quantidade`  | Envia uma solicitação para finalizar a compra dos produtos no carrinho. |
| `SAIR`           | Nenhum                         | Finaliza a sessão do cliente e desconecta do servidor.            |

### Respostas do Servidor
| Código de Resposta | Descrição                                                         |
|--------------------|-------------------------------------------------------------------|
| `PROD-220`         | Lista de produtos, incluindo ID, Nome, Preço e Quantidade.        |
| `CATE-221`         | Lista de categorias.                                              |
| `ERRO-305`         | Mensagem de erro genérico para métodos não encontrados ou inválidos.|

## Instruções para Execução

Siga os passos abaixo para executar a aplicação cliente-servidor:

### 1. Executar o Servidor
No terminal, acesse o diretório do projeto e execute o seguinte comando para iniciar o servidor:
/```bash
python servidor.py

Após isso, o servidor será aberto

### 2. Executar o Cliente
/```bash
python cliente.py

Após isso, o cliente será  aberto e será conectado ao servidor

