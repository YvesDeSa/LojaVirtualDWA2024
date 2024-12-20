SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco FLOAT NOT NULL,
        descricao TEXT NOT NULL,
        estoque INTEGER NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categoria(id))
"""

SQL_INSERIR = """
    INSERT INTO produto (nome, preco, descricao, estoque, categoria_id)
    VALUES (?, ?, ?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, preco, descricao, estoque, categoria_id
    FROM produto
    ORDER BY nome
"""

SQL_ALTERAR = """
    UPDATE produto
    SET nome=?, preco=?, descricao=?, estoque=?, categoria_id=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM produto    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, nome, preco, descricao, estoque, categoria_id
    FROM produto
    WHERE id=?
"""

SQL_OBTER_POR_CATEGORIA = """
    SELECT id, nome, preco, descricao, estoque, categoria_id
    FROM produto
    WHERE categoria_id=?
    ORDER BY nome
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) FROM produto
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome, preco, descricao, estoque, categoria_id
    FROM produto
    WHERE nome LIKE ? OR descricao LIKE ?
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) FROM produto
    WHERE nome LIKE ? OR descricao LIKE ?
"""

SQL_OBTER_BUSCA_POR_CATEGORIA = """
    SELECT id, nome, preco, descricao, estoque, categoria_id
    FROM produto
    WHERE categoria_id=? AND (nome LIKE ? OR descricao LIKE ?)
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA_CATEGORIA = """
    SELECT COUNT(*) FROM produto
    WHERE categoria_id=? AND (nome LIKE ? OR descricao LIKE ?)
"""