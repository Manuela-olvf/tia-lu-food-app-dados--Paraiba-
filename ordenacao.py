# ordenacao.py - Implementação do algoritmo de ordenação Bucket Sort

def bucket_sort(lista_dados, extrator_chave, num_baldes=10):
    """
    Ordena uma lista de dicionários (mapas) usando o Bucket Sort.
    
    Args:
        lista_dados (list): Lista de mapas (e.g., Pedidos) a ser ordenada.
        extrator_chave (callable): Função que recebe um item e retorna a chave (e.g., lambda p: p['codigo']).
        num_baldes (int): Número de 'baldes'.
    """
    if not lista_dados:
        return []

    # 1. Encontra os valores min e max da chave
    try:
        min_chave = min(extrator_chave(item) for item in lista_dados)
        max_chave = max(extrator_chave(item) for item in lista_dados)
    except (ValueError, TypeError):
        print("Erro ao extrair chaves. Verifique se a chave é numérica.")
        return lista_dados # Retorna a lista original se houver erro

    if min_chave == max_chave:
        return lista_dados # Todos os elementos são iguais

    # 2. Inicializa os baldes
    baldes = [[] for _ in range(num_baldes)]
    
    # +1 para incluir o max_chave no range
    tamanho_intervalo = (max_chave - min_chave + 1) / num_baldes
    
    if tamanho_intervalo == 0: 
        tamanho_intervalo = 1

    # 3. Distribui os elementos nos baldes
    for item in lista_dados:
        chave = extrator_chave(item)
        
        # Calcula o índice do balde
        indice_balde = int((chave - min_chave) // tamanho_intervalo)
        
        # Garante que o índice não exceda o limite (para o max_chave)
        indice_balde = min(indice_balde, num_baldes - 1)
        
        baldes[indice_balde].append(item)

    # 4. Ordena os baldes individualmente e concatena
    lista_ordenada = []
    for balde in baldes:
        # Usamos o sort nativo do Python (Timsort) para ordenar os baldes
        balde.sort(key=extrator_chave)
        lista_ordenada.extend(balde)
        
    return lista_ordenada