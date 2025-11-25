"""
Módulo de gerenciamento de reservas.
Contém funções para criar, cancelar e gerenciar reservas.
"""

from datetime import datetime
from calculo import calcular_valor_reserva, calcular_dias_estadia, verificar_disponibilidade
from interface import coletar_dados_reserva
from arquivo import salvar_reservas


def gerar_hash_reserva(dados_reserva):
    """
    Gera um código hash único para a reserva.
    
    Args:
        dados_reserva (dict): Dados da reserva
        
    Returns:
        int: Código hash positivo
    """
    return abs(hash(str(dados_reserva)))


def criar_reserva(reservas):
    """
    Cria uma nova reserva após coletar dados e validar disponibilidade.
    
    Args:
        reservas (list): Lista de reservas existentes
        
    Returns:
        bool: True se a reserva foi criada com sucesso, False caso contrário
    """
    dados = coletar_dados_reserva()
    
    if not dados:
        print("\nErro ao coletar dados da reserva.")
        return False
    
    # Verifica disponibilidade
    disponivel = verificar_disponibilidade(
        reservas,
        dados['tipo_quarto'],
        dados['checkin'],
        dados['checkout'],
        dados['quantidade_quartos']
    )
    
    if not disponivel:
        print("\n" + "="*60)
        print("NÃO FOI POSSÍVEL REALIZAR ESSA RESERVA!")
        print("="*60)
        print("Não há quartos suficientes disponíveis para o período solicitado.")
        print("Sugestões:")
        print("  - Escolha outro tipo de quarto")
        print("  - Reduza a quantidade de quartos")
        print("  - Altere as datas da reserva")
        print("="*60 + "\n")
        return False
    
    # Calcula valor da reserva
    dias_estadia = calcular_dias_estadia(dados['checkin'], dados['checkout'])
    valor = calcular_valor_reserva(
        dados['tipo_quarto'],
        dados['quantidade_quartos'],
        dias_estadia
    )
    
    # Cria a reserva completa
    reserva = {
        'hash': gerar_hash_reserva(dados),
        'nome': dados['nome'],
        'checkin': dados['checkin'],
        'checkout': dados['checkout'],
        'tipo_quarto': dados['tipo_quarto'],
        'quantidade_quartos': dados['quantidade_quartos'],
        'valor': valor
    }
    
    # Adiciona à lista e salva
    reservas.append(reserva)
    
    if salvar_reservas(reservas):
        print("\n" + "="*60)
        print("RESERVA REALIZADA COM SUCESSO!")
        print("="*60)
        print(f"Código da Reserva: {reserva['hash']}")
        print(f"Responsável: {reserva['nome']}")
        print(f"Período: {reserva['checkin'].strftime('%d/%m/%Y')} a {reserva['checkout'].strftime('%d/%m/%Y')}")
        print(f"Valor Total: R$ {valor:.2f}")
        print("="*60 + "\n")
        return True
    else:
        # Remove da lista se não conseguiu salvar
        reservas.pop()
        print("\nErro ao salvar a reserva. Tente novamente.")
        return False


def cancelar_reserva(reservas):
    """
    Cancela uma reserva existente baseado no código hash.
    
    Args:
        reservas (list): Lista de reservas existentes
        
    Returns:
        bool: True se a reserva foi cancelada, False caso contrário
    """
    print("\n" + "="*60)
    print("CANCELAR RESERVA")
    print("="*60 + "\n")
    
    try:
        codigo_hash = int(input("Digite o código (HASH) da reserva: "))
    except ValueError:
        print("\nErro! Digite um código válido.")
        return False
    
    # Busca a reserva
    for indice, reserva in enumerate(reservas):
        if reserva['hash'] == codigo_hash:
            # Verifica se a reserva já passou
            if reserva['checkout'] < datetime.today():
                print("\n" + "="*60)
                print("ESSA RESERVA NÃO PODE SER CANCELADA!")
                print("="*60)
                print("O período da reserva já foi concluído.")
                print("="*60 + "\n")
                return False
            
            # Remove a reserva
            reservas.pop(indice)
            
            if salvar_reservas(reservas):
                print("\n" + "="*60)
                print("RESERVA CANCELADA COM SUCESSO!")
                print("="*60)
                print(f"Código: {codigo_hash}")
                print(f"Responsável: {reserva['nome']}")
                print("="*60 + "\n")
                return True
            else:
                # Restaura a reserva se não conseguiu salvar
                reservas.insert(indice, reserva)
                print("\nErro ao salvar as alterações. Tente novamente.")
                return False
    
    print(f"\nReserva com código {codigo_hash} não encontrada.")
    return False
