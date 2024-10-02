class Sql:
    """
    Classe Sql que contém métodos para retornar consultas SQL utilizadas no sistema de estoque.

    Os métodos desta classe retornam comandos SQL para buscar produtos e categorias no banco de dados.
    """

    @classmethod
    def produtos_por_categoria(cls) -> str:
        """
        Retorna uma string com a consulta SQL que seleciona produtos pertencentes a uma determinada categoria.

        A consulta utiliza um JOIN entre as tabelas 'Produtos' e 'Categoria', filtrando os produtos
        pela categoria fornecida como parâmetro.

        Returns:
            str: Comando SQL que retorna produtos de uma categoria específica.
        """
        return '''
                SELECT Produtos.id, Produtos.nome, Produtos.preco, Produtos.quantidade
                FROM Produtos
                JOIN Categoria ON Produtos.categoria_id = Categoria.id
                WHERE Categoria.nome = ?
                '''
    
    @classmethod
    def categorias(cls) -> str:
        """
        Retorna uma string com a consulta SQL que seleciona os nomes de todas as categorias presentes no banco de dados.

        Returns:
            str: Comando SQL que retorna todos os nomes das categorias.
        """
        return 'SELECT nome FROM Categoria'