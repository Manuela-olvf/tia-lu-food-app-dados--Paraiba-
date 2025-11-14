#guarda as funções que mexem com o arquivo JSON
import json

def carregar_dados(caminho_arquivo="dados.json"):
    """
    Carrega os dados do arquivo JSON especificado.
    Caso o arquivo não exista, cria uma nova estrutura padrão.
    """
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Arquivo de dados não encontrado. Criando novo arquivo...")
        return {"itens": [], "pedidos": []}


def salvar_dados(dados, caminho_arquivo="dados.json"):
    """
    Salva os dados no arquivo JSON especificado de forma legível (indentado).
    """
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
