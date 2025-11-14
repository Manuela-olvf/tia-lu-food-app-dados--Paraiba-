# main.py - Ponto de entrada do sistema 

# Importa os módulos criados
import utils
import gerenciador_menu
import gerenciador_pedidos
import os

def limpar_tela():
    """Limpa o console."""
    # 'cls' para Windows, 'clear' para Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')

def inicializar_sistema():
    """Carrega dados do JSON e os popula nas AVL Trees."""
    limpar_tela()
    print("--- Inicializando Sistema Tia Lu Food App ---")
    
    # 1. Carrega dados do utils.py
    # A função carregar_dados() já retorna {'itens': [], 'pedidos': []} se o arquivo não existir
    dados = utils.carregar_dados() 
    
    # 2. Popula as Árvores AVL (os gerenciadores fazem isso)
    # Passamos as duas listas para que os gerenciadores possam salvar corretamente
    gerenciador_menu.inicializar_menu(dados.get('itens', []), dados.get('pedidos', []))
    gerenciador_pedidos.inicializar_pedidos(dados.get('pedidos', []), dados.get('itens', []))
    
    print("\nSistema pronto!")
    input("Pressione ENTER para continuar...")

# --- Funções de Interface (Menu Cardápio) ---

def menu_cadastro_item():
    """Interface para cadastrar um novo item."""
    limpar_tela()
    print("--- Cadastro de Novo Item ---")
    try:
        nome = input("Nome do item: ")
        descricao = input("Descrição: ")
        preco = float(input("Preço (R$): ").replace(',', '.'))
        estoque = int(input("Quantidade em estoque: "))
        
        if preco < 0 or estoque < 0:
            raise ValueError("Valores não podem ser negativos.")
        
        if not nome or not descricao:
             raise ValueError("Nome e descrição não podem ser vazios.")
            
        # Chama a função do gerenciador
        item = gerenciador_menu.registrar_item(nome, descricao, preco, estoque)
        print(f"\nItem '{item['nome']}' (Cód: {item['codigo']}) cadastrado com sucesso!")
        
    except ValueError as e:
        print(f"\nErro de entrada: {e}. O item não foi cadastrado.")

def menu_consultar_itens():
    """Consulta e exibe todos os itens do cardápio."""
    limpar_tela()
    # Chama a função do gerenciador
    itens = gerenciador_menu.get_itens_menu()
    if not itens:
        print("Não há itens cadastrados.")
        return
        
    print("--- Cardápio Tia Lu ---")
    print("{:<5} | {:<25} | {:<10} | {:<10}".format("CÓD", "NOME", "PREÇO (R$)", "ESTOQUE"))
    print("-" * 60)
    for item in itens:
        print("{:<5} | {:<25} | {:<10.2f} | {:<10}".format(
            item['codigo'], item['nome'], item['preco'], item['estoque']
        ))

def menu_atualizar_item():
    """Atualiza um item existente."""
    menu_consultar_itens() # Mostra a lista primeiro
    if not gerenciador_menu.get_itens_menu():
        return
        
    try:
        codigo = int(input("\nDigite o código do item para atualizar: "))
        # Busca o item usando o gerenciador
        item = gerenciador_menu.buscar_item_por_codigo(codigo)
        
        if not item:
            print("Item não encontrado.")
            return

        print(f"\nAtualizando: {item['nome']} (Deixe em branco para manter o valor atual)")
        nome = input(f"Novo nome ({item['nome']}): ") or None
        desc = input(f"Nova descrição ({item['descricao']}): ") or None
        
        preco_str = input(f"Novo preço ({item['preco']}): ")
        preco = float(preco_str.replace(',', '.')) if preco_str else None
        
        estoque_str = input(f"Novo estoque ({item['estoque']}): ")
        estoque = int(estoque_str) if estoque_str else None
        
        # Chama a função de atualização do gerenciador
        gerenciador_menu.atualizar_detalhes_item(codigo, nome, desc, preco, estoque)
        print("Item atualizado com sucesso!")

    except ValueError:
        print("Entrada inválida (código, preço ou estoque).")

# --- Funções de Interface (Menu Pedidos) ---

def menu_criar_pedido():
    """Interface para criar um novo pedido."""
    limpar_tela()
    menu_consultar_itens() # Mostra o cardápio
    print("\n--- Criar Novo Pedido ---")
    
    itens_pedido = [] # Lista de tuplas