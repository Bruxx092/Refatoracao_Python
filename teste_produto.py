from models.produto_model import ProdutoModel

def testar_produto_model():
    try:
        ProdutoModel.criar_tabela()
        
        id1 = ProdutoModel.inserir_produto(
            nome="Notebook Gamer_novo", 
            preco=5500.90,
            descricao="Notbook i7 16GB RAM RTX 3060",
            estoque=5
        )
        id2 = ProdutoModel.inserir_produto(
            nome="Mouse Com Fio", 
            preco=129.90,
            estoque=20
        )
        
        produto = ProdutoModel.buscar_por_id(id1)
        print(produto)
        
        for p in ProdutoModel.listar_produtos():
            print(f"{p['produto_id']}: {p['nome']} - R${p['preco']:.2f}")
        
        ProdutoModel.atualizar_produto(
            produto_id=id1,
            preco=5200.00
        )
        
        novo_estoque = ProdutoModel.ajustar_estoque(id1, 10)
        print(f"Novo estoque: {novo_estoque}")
        
        ProdutoModel.remover_produto(id2)
        
    except Exception as e:
        print(f"ERRO: {str(e)}")

if __name__ == "__main__":
    testar_produto_model()