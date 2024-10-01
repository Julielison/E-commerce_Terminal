class Sql:
    @classmethod
    def produtos_por_categoria(cls):
        return '''
                SELECT Produtos.id, Produtos.nome, Produtos.preco, Produtos.quantidade
                FROM Produtos
                JOIN Categoria ON Produtos.categoria_id = Categoria.id
                WHERE Categoria.nome = ?
                '''
    
    @classmethod
    def categorias(cls):
        return 'SELECT nome FROM Categoria'