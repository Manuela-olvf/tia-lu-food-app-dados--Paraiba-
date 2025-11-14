# indexador_avl.py - Implementação da Árvore AVL

class No:
    """Nó da Árvore AVL. Armazena a chave e os dados (mapa)."""
    def __init__(self, chave, dados):
        self.chave = chave  # Chave (e.g., código do item/pedido)
        self.dados = dados  # Dados (o "mapa" - dicionário do item/pedido)
        self.altura = 1
        self.esquerda = None
        self.direita = None

class ArvoreAvl:
    """Implementação da Árvore AVL."""
    def __init__(self):
        self.raiz = None

    def _get_altura(self, no):
        """Retorna a altura do nó (0 se for None)."""
        if not no:
            return 0
        return no.altura

    def _get_fator_balanceamento(self, no):
        """Calcula o fator de balanceamento (Altura_Esquerda - Altura_Direita)."""
        if not no:
            return 0
        return self._get_altura(no.esquerda) - self._get_altura(no.direita)

    def _atualizar_altura(self, no):
        """Recalcula a altura de um nó."""
        if not no:
            return
        no.altura = 1 + max(self._get_altura(no.esquerda), self._get_altura(no.direita))

    # --- Rotações ---
    def _rotacao_direita(self, y):
        """Rotação simples à direita."""
        x = y.esquerda
        T2 = x.direita
        x.direita = y
        y.esquerda = T2
        self._atualizar_altura(y)
        self._atualizar_altura(x)
        return x

    def _rotacao_esquerda(self, x):
        """Rotação simples à esquerda."""
        y = x.direita
        T1 = y.esquerda
        y.esquerda = x
        x.direita = T1
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        return y

    # --- Funções Públicas ---
    
    def inserir(self, chave, dados):
        """Interface pública para inserir um nó."""
        self.raiz = self._inserir_recursivo(self.raiz, chave, dados)

    def _inserir_recursivo(self, raiz, chave, dados):
        """Função recursiva para inserção e balanceamento."""
        # 1. Inserção normal da BST
        if not raiz:
            return No(chave, dados)
        elif chave < raiz.chave:
            raiz.esquerda = self._inserir_recursivo(raiz.esquerda, chave, dados)
        elif chave > raiz.chave:
            raiz.direita = self._inserir_recursivo(raiz.direita, chave, dados)
        else:
            # Chave já existe, apenas atualiza os dados
            raiz.dados = dados
            return raiz

        # 2. Atualiza a altura
        self._atualizar_altura(raiz)

        # 3. Calcula o balanceamento
        balanceamento = self._get_fator_balanceamento(raiz)

        # 4. Aplica rotações se estiver desbalanceado
        
        # Caso Esquerda-Esquerda (LL)
        if balanceamento > 1 and chave < raiz.esquerda.chave:
            return self._rotacao_direita(raiz)

        # Caso Direita-Direita (RR)
        if balanceamento < -1 and chave > raiz.direita.chave:
            return self._rotacao_esquerda(raiz)

        # Caso Esquerda-Direita (LR)
        if balanceamento > 1 and chave > raiz.esquerda.chave:
            raiz.esquerda = self._rotacao_esquerda(raiz.esquerda)
            return self._rotacao_direita(raiz)

        # Caso Direita-Esquerda (RL)
        if balanceamento < -1 and chave < raiz.direita.chave:
            raiz.direita = self._rotacao_direita(raiz.direita)
            return self._rotacao_esquerda(raiz)

        return raiz

    def buscar(self, chave):
        """Busca um item pela chave e retorna o dicionário de dados (o mapa)."""
        return self._buscar_recursivo(self.raiz, chave)

    def _buscar_recursivo(self, raiz, chave):
        """Função recursiva para busca."""
        if not raiz:
            return None
        if raiz.chave == chave:
            return raiz.dados
        elif chave < raiz.chave:
            return self._buscar_recursivo(raiz.esquerda, chave)
        else:
            return self._buscar_recursivo(raiz.direita, chave)
            
    def atualizar_dados(self, chave, novo_mapa_dados):
        """Atualiza os dados de um nó existente."""
        no = self._encontrar_no(self.raiz, chave)
        if no:
            no.dados.update(novo_mapa_dados) # Atualiza o dicionário/mapa
            return True
        return False
    
    def _encontrar_no(self, raiz, chave):
        """Encontra e retorna o objeto No."""
        if not raiz or raiz.chave == chave:
            return raiz
        elif chave < raiz.chave:
            return self._encontrar_no(raiz.esquerda, chave)
        else:
            return self._encontrar_no(raiz.direita, chave)

    def percorrer_em_ordem(self):
        """Retorna todos os 'dados' (mapas) em ordem de chave."""
        resultado = []
        self._percorrer_em_ordem_recursivo(self.raiz, resultado)
        return resultado

    def _percorrer_em_ordem_recursivo(self, raiz, resultado):
        if raiz:
            self._percorrer_em_ordem_recursivo(raiz.esquerda, resultado)
            resultado.append(raiz.dados)
            self._percorrer_em_ordem_recursivo(raiz.direita, resultado)

    def get_max_chave(self):
        """Encontra a maior chave (para sabermos o próximo ID)."""
        if not self.raiz:
            return 0
        atual = self.raiz
        while atual.direita is not None:
            atual = atual.direita
        return atual.chave