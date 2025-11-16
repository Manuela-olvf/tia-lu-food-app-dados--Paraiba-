from utils import carregar_dados, salvar_dados
from ordenacao import bucket_sort
from indexador_avl import ArvoreAvl
dados = carregar_dados()
#Criamos a árvore AVL que vai armazenar os itens
# Isso permite busca mais rápida pelo código do item.
arvore_itens = ArvoreAvl()
for item in dados["itens"]:
    arvore_itens.inserir(item["codigo"], item)

# A função a seguir cria um novo item no menu e salva no JSON + AVL

def registrar_item():
    print("\n=== Cadastro de Novo Item ===")
    #Nesse parte do código pedimos ao usiario para inserir as informações do item
    # O código serve como chave principal para buscas na AVL.
    codigo = int(input("Código do item: "))
    nome = input("Nome do item: ")
    descricao = input("Descrição: ")
    preco = float(input("Preço: "))
    estoque = int(input("Estoque inicial: "))

    # Criamos o item como um MAPA (dicionário)
    item = {
        "codigo": codigo,
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "estoque": estoque
    }

    # Adicionamos na lista em memória
    dados["itens"].append(item)

    # Inserimos o item na árvore AVL
    arvore_itens.inserir(codigo, item)

    # Salvamos tudo no JSON para persistência permanente
    salvar_dados(dados)

    print("Item registrado com sucesso!")

# Em seguida vamos exibir todos os itens do menu ordenados por código

def listar_itens():
    print("\n=== Lista de Itens ===")
    
    itens_ordenados = sorted(dados["itens"], key=lambda x: x["codigo"])

    # Exibe item a item
    for item in itens_ordenados:
        print(f"""
Código: {item['codigo']}
Nome: {item['nome']}
Descrição: {item['descricao']}
Preço: R${item['preco']:.2f}
Estoque: {item['estoque']} """)
        
def atualizar_item():
    print("\n=== Atualização de Item ===")
    codigo = int(input("Informe o código do item: "))

    # Busca rápida usando AVL
    item = arvore_itens.buscar(codigo)

    if not item:
        print("Item não encontrado!")
        return

    print("Deixe em branco caso não queira alterar:")

    novo_nome = input(f"Novo nome (atual: {item['nome']}): ")
    novo_desc = input(f"Nova descrição (atual: {item['descricao']}): ")
    novo_preco = input(f"Novo preço (atual: {item['preco']}): ")
    novo_estoque = input(f"Novo estoque (atual: {item['estoque']}): ")

    # Atualiza apenas os campos que foram preenchidos
    if novo_nome:
        item["nome"] = novo_nome
    if novo_desc:
        item["descricao"] = novo_desc
    if novo_preco:
        item["preco"] = float(novo_preco)
    if novo_estoque:
        item["estoque"] = int(novo_estoque)

    # Atualiza JSON
    salvar_dados(dados)

    print("Item atualizado com sucesso!")

# Função de remover itens da lista 

def remover_item():
    print("\n=== Remoção de Item ===")
    codigo = int(input("Código do item a remover: "))

    # Remove da lista em memória
    item_removido = False
    for i, item in enumerate(dados["itens"]):
        if item["codigo"] == codigo:
            dados["itens"].pop(i)
            item_removido = True
            break

    if not item_removido:
        print("Item não encontrado!")
        return

    # Remove da AVL
    arvore_itens.delete(codigo)

    # Atualiza JSON
    salvar_dados(dados)

    print("Item removido com sucesso!")

#Criando a função do menu. 
def menu_gerenciador_menu():
    while True:
        print("""
======== GERENCIADOR DE MENU ========
1 - Registrar item
2 - Listar itens
3 - Atualizar item
4 - Remover item
0 - Voltar ao menu principal
""")

        opc = input("Escolha: ")

        if opc == "1":
            registrar_item()
        elif opc == "2":
            listar_itens()
        elif opc == "3":
            atualizar_item()
        elif opc == "4":
            remover_item ()
        elif opc == "0":
            break
        else:
            print("Opção inválida!")
