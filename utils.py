"""
Módulo de utilitários gerais.
Contém funções auxiliares usadas em todo o sistema.
"""

import os


def limpar_terminal():
    """
    Limpa a tela do terminal de forma compatível com o Sistema Operacional.
    """
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")


def formatar_valor_monetario(valor):
    """
    Formata um valor numérico como moeda brasileira.
    
    Args:
        valor (float): Valor a ser formatado
        
    Returns:
        str: Valor formatado como R$ X.XXX,XX
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def validar_entrada_inteira(mensagem, minimo=None, maximo=None):
    """
    Solicita e valida uma entrada inteira do usuário.
    
    Args:
        mensagem (str): Mensagem a ser exibida
        minimo (int, optional): Valor mínimo aceito
        maximo (int, optional): Valor máximo aceito
        
    Returns:
        int: Valor inteiro validado
    """
    while True:
        try:
            valor = int(input(mensagem))
            
            if minimo is not None and valor < minimo:
                print(f"Erro! O valor deve ser maior ou igual a {minimo}.")
                continue
                
            if maximo is not None and valor > maximo:
                print(f"Erro! O valor deve ser menor ou igual a {maximo}.")
                continue
                
            return valor
        except ValueError:
            print("Erro! Digite um número inteiro válido.")
