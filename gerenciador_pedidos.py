from indexador_avl import ArvoreAvl
from gerenciador_menu import arvore_itens
from ordenacao import bucket_sort
import utils
import gerenciador_menu

# Status
STATUS_AGUARDANDO = "AGUARDANDO_APROVACAO"
STATUS_ACEITO = "ACEITO"
STATUS_FAZENDO = "FAZENDO"
STATUS_PRONTO = "PRONTO"
STATUS_ENTREGUE = "ENTREGUE"
STATUS_REJEITADO = "REJEITADO"
STATUS_CANCELADO = "CANCELADO"

# Dados e estruturas
dados = {}
pedidos_list = []          # lista para salvar alterações no JSON
avl_pedidos = ArvoreAvl()  # AVL em memória para buscas rápidas


# Inicialização
# Carrega dados do JSON e popula a AVL.
def inicializar_pedidos(pedidos_from_main=None, itens_from_main=None):
    global dados, pedidos_list, avl_pedidos

    dados = utils.carregar_dados()

    if 'pedidos' not in dados:
        dados['pedidos'] = []
    if 'itens' not in dados:
        dados['itens'] = []

    pedidos_list = dados['pedidos']

    # popula AVL (substitui a árvore anterior)
    avl_pedidos = ArvoreAvl()
    for p in pedidos_list:
        chave = p.get('id')
        if chave is None:
            continue
        avl_pedidos.inserir(chave, p)


# Salvando o dicionário 'dados' no JSON.
def _salvar():
    dados['pedidos'] = pedidos_list
    utils.salvar_dados(dados)

# Busca o código do item direto no gerenciador_menu
def _buscar_item_por_codigo(codigo):
    item = arvore_itens.buscar(codigo)

    if not item:
        print("Item não encontrado!")
        return

# Retorna o próximo código baseado na maior chave da AVL.
def _proximo_codigo():
    max_chave = avl_pedidos.get_max_chave()
    return (max_chave or 0) + 1

def _inserir_pedido_no_sistema(pedido):
    """Insere pedido na AVL e na lista + salva JSON."""
    pedidos_list.append(pedido)
    avl_pedidos.inserir(pedido['id'], pedido)
    _salvar()

# Atualiza o pedido armazenado: altera os dados da AVL e salva no JSON
def _atualizar_pedido_no_sistema(chave, novo_mapa):
    ok = avl_pedidos.atualizar_dados(chave, novo_mapa)

    if ok:
        _salvar()  # salva pedidos_list no arquivo

    return ok


# CRIANDO PEDIDOS
#Cria um pedido via input do usuário, reserva estoque e salva.
def criar_pedido():
    if not dados.get('itens'):
        print("Não há itens no cardápio para criar pedido.")
        return None

    itens_pedido = []

    while True:
        # Mostrar cardápio
        menu_itens = gerenciador_menu.get_itens_menu()
        print("\n--- CARDÁPIO ---")
        for it in menu_itens:
            print(f"{it['codigo']} - {it['nome']} - R${it['preco']:.2f} - Estoque: {it.get('estoque',0)}")

        # Escolher item
        try:
            codigo_item = int(input("Digite o código do item que deseja adicionar: "))
        except ValueError:
            print("Código inválido.")
            continue

        item = _buscar_item_por_codigo(codigo_item)
        if not item:
            print("Item não encontrado.")
            continue

        # Quantidade
        try:
            quantidade = int(input("Quantidade: "))
        except ValueError:
            print("Quantidade inválida.")
            continue

        if item.get('estoque', 0) < quantidade:
            print("Estoque insuficiente.")
            continue

        # Adicionar ao pedido
        itens_pedido.append({
            'codigo': codigo_item,
            'quantidade': quantidade,
            'preco_unit': item.get('preco', 0)
        })

        # diminuir estoque
        item['estoque'] -= quantidade

        mais = input("Deseja adicionar outro item? (s/n): ").strip().lower()
        if mais != 's':
            break

    # Se nenhum item foi adicionado
    if not itens_pedido:
        print("Nenhum item selecionado. Pedido cancelado.")
        return None

    # Total
    total = sum(it['quantidade'] * it['preco_unit'] for it in itens_pedido)

    cupom = input("Deseja aplicar cupom de desconto (%)? Caso não, pressione enter: ").strip()
    if cupom:
        try:
            desconto = float(cupom)
            total = total * (1 - desconto / 100)
        except ValueError:
            print("Cupom inválido. Nenhum desconto aplicado.")

    # Finalizando a criação do pedido
    novo_id = _proximo_codigo()
    pedido = {
        'id': novo_id,
        'itens': itens_pedido,
        'total': round(total, 2),
        'status': STATUS_AGUARDANDO
    }

    # Salvando na AVL e no JSON
    avl_pedidos.inserir(novo_id, pedido)
    pedidos_list.append(pedido)

    _salvar()

    print(f"\nPedido {novo_id} criado com sucesso! Total: R${pedido['total']:.2f}")
    return pedido


# Usamos o algoritmo de ordenação - Bucket Sort para listar os pedidos
def listar_pedidos(status=None, ordenado_por_id=False, ordenado_por_total=False):

    # Bucket sort é aplicado apenas quando ordenado_por_id ou ordenado_por_total for True
    
    resultado = pedidos_list if status is None else [p for p in pedidos_list if p.get('status') == status]

    if ordenado_por_id:
        resultado = bucket_sort(resultado, lambda x: x.get('id', 0))
    if ordenado_por_total:
        resultado = bucket_sort(resultado, lambda x: x.get('total', 0))

    return resultado

# Lista os pedidos criados
def listar_pedidos():
    lista = listar_pedidos()
    if not lista:
        print("Não há pedidos.")
        return
    for p in lista:
        print_pedido(p)

# Buscando pedidos por id
#Retorna um mapa do pedido de acordo com o id
def print_pedido(pedido):
    print("\n--- PEDIDO ---")
    print(f"ID: {pedido.get('id')}")
    print(f"Status: {pedido.get('status')}")
    print(f"Total: R${pedido.get('total'):.2f}")
    print("Itens:")
    for it in pedido.get('itens', []):
        item_info = _buscar_item_por_codigo(it['codigo'])
        nome = item_info.get('nome') if item_info else f"Código {it['codigo']}"
        print(f"- {nome} x{it['quantidade']} (R${it.get('preco_unit'):.2f})")

def buscar_pedido_por_id(pid):
    #Busca via AVL (mais rápido) e retorna o mapa do pedido.
    res = avl_pedidos.buscar(pid)
    return res

#CONSULTANDO PEDIDOS
def menu_consultar_pedidos():
    print("\n--- CONSULTAR PEDIDOS ---")
    escolha = input("Deseja buscar por ID (i) ou listar todos (t)? ").strip().lower()

    if escolha == 'i':
        try:
            pid = int(input("Digite o ID do pedido: "))
        except ValueError:
            print("ID inválido.")
            return
        pedido = buscar_pedido_por_id(pid)
        if pedido:
            print_pedido(pedido)
        else:
            print("Pedido não encontrado.")
    elif escolha == 't':
        pedidos = listar_pedidos()
        if not pedidos:
            print("Não há pedidos cadastrados.")
        else:
            for p in pedidos:
                print_pedido(p)
    else:
        print("Opção inválida.")

# PROCESSANDO PEDIDOS PENDENTES
def processar_pedidos_pendentes():
    pendentes = [p for p in pedidos_list if p.get('status') == STATUS_AGUARDANDO]
    if not pendentes:
        print("Não há pedidos pendentes.")
        return

    for p in pendentes:
        print_pedido(p)
        acao = input("Aceitar ou Rejeitar o pedido? (a/r): ").strip().lower()
        if acao == 'a':
            _atualizar_pedido_no_sistema(p['id'], {'status': STATUS_ACEITO})
            print(f"Pedido {p['id']} ACEITO.")
        elif acao == 'r':
            _atualizar_pedido_no_sistema(p['id'], {'status': STATUS_REJEITADO})
            print(f"Pedido {p['id']} REJEITADO.")
        else:
            print("Ação inválida. Pulando.")