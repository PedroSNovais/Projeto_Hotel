"""
Módulo responsável pela persistência de dados.
Gerencia carregamento e salvamento de reservas em arquivo.
"""

import os
import pickle
from config import DIRETORIO_DADOS, ARQUIVO_RESERVAS


def obter_caminho_arquivo():
    """
    Retorna o caminho completo do arquivo de reservas.
    
    Returns:
        str: Caminho completo do arquivo
    """
    return os.path.join(DIRETORIO_DADOS, ARQUIVO_RESERVAS)


def garantir_diretorio_existe():
    """
    Garante que o diretório de dados existe, criando-o se necessário.
    """
    if not os.path.exists(DIRETORIO_DADOS):
        os.makedirs(DIRETORIO_DADOS)


def carregar_reservas():
    """
    Carrega as reservas do arquivo pickle.
    Se o arquivo não existir, cria um novo e retorna lista vazia.
    
    Returns:
        list: Lista de dicionários contendo as reservas
    """
    caminho = obter_caminho_arquivo()
    
    if os.path.exists(caminho):
        try:
            with open(caminho, "rb") as arquivo:
                return pickle.load(arquivo)
        except (pickle.PickleError, EOFError) as erro:
            print(f"Erro ao carregar reservas: {erro}")
            return []
    else:
        garantir_diretorio_existe()
        salvar_reservas([])
        return []


def salvar_reservas(reservas):
    """
    Salva a lista de reservas no arquivo pickle.
    
    Args:
        reservas (list): Lista de dicionários contendo as reservas
        
    Returns:
        bool: True se salvou com sucesso, False caso contrário
    """
    garantir_diretorio_existe()
    caminho = obter_caminho_arquivo()
    
    try:
        with open(caminho, "wb") as arquivo:
            pickle.dump(reservas, arquivo)
        return True
    except (pickle.PickleError, IOError) as erro:
        print(f"Erro ao salvar reservas: {erro}")
        return False
