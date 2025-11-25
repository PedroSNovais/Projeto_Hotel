"""
Módulo de cálculos e validações.
Contém funções para cálculo de valores, estatísticas e validação de reservas.
"""

from config import QUARTOS_QUANTIDADE, QUARTOS_VALOR


def calcular_valor_reserva(tipo_quarto, quantidade_quartos, dias_estadia):
    """
    Calcula o valor total de uma reserva.
    
    Args:
        tipo_quarto (str): Tipo do quarto (standard, premium, luxo)
        quantidade_quartos (int): Quantidade de quartos
        dias_estadia (int): Número de dias da estadia
        
    Returns:
        float: Valor total da reserva
    """
    valor_diaria = QUARTOS_VALOR[tipo_quarto]
    valor_total = valor_diaria * dias_estadia * quantidade_quartos
    return valor_total


def calcular_dias_estadia(data_checkin, data_checkout):
    """
    Calcula o número de dias entre check-in e check-out.
    
    Args:
        data_checkin (datetime): Data de check-in
        data_checkout (datetime): Data de check-out
        
    Returns:
        int: Número de dias de estadia
    """
    return (data_checkout - data_checkin).days


def verificar_disponibilidade(reservas, tipo_quarto, data_checkin, data_checkout, quantidade_solicitada):
    """
    Verifica se há quartos disponíveis para o período solicitado.
    
    Args:
        reservas (list): Lista de reservas existentes
        tipo_quarto (str): Tipo do quarto desejado
        data_checkin (datetime): Data de check-in
        data_checkout (datetime): Data de check-out
        quantidade_solicitada (int): Quantidade de quartos solicitados
        
    Returns:
        bool: True se há disponibilidade, False caso contrário
    """
    quartos_ocupados = 0
    
    for reserva in reservas:
        if reserva['tipo_quarto'] == tipo_quarto:
            # Verifica se há sobreposição de datas
            if data_checkin < reserva['checkout'] and data_checkout > reserva['checkin']:
                quartos_ocupados += reserva['quantidade_quartos']
    
    quartos_disponiveis = QUARTOS_QUANTIDADE[tipo_quarto] - quartos_ocupados
    
    return quartos_disponiveis >= quantidade_solicitada


def calcular_estatisticas(reservas):
    """
    Calcula estatísticas gerais sobre as reservas.
    
    Args:
        reservas (list): Lista de reservas
        
    Returns:
        dict: Dicionário com as estatísticas ou None se não houver reservas
    """
    if not reservas:
        return None
    
    quantidade_reservas = len(reservas)
    reserva_mais_cara = reservas[0]
    reserva_mais_longa = reservas[0]
    dias_mais_longa = calcular_dias_estadia(
        reserva_mais_longa['checkin'],
        reserva_mais_longa['checkout']
    )
    
    quartos_reservados = {
        "standard": 0,
        "premium": 0,
        "luxo": 0
    }
    
    soma_total_valores = 0.0
    
    for reserva in reservas:
        # Atualiza reserva mais cara
        if reserva["valor"] > reserva_mais_cara["valor"]:
            reserva_mais_cara = reserva
        
        # Atualiza reserva mais longa
        dias_reserva = calcular_dias_estadia(reserva['checkin'], reserva['checkout'])
        if dias_reserva > dias_mais_longa:
            reserva_mais_longa = reserva
            dias_mais_longa = dias_reserva
        
        # Conta quartos reservados por tipo
        quartos_reservados[reserva["tipo_quarto"]] += reserva["quantidade_quartos"]
        
        # Soma valores
        soma_total_valores += reserva["valor"]
    
    return {
        'quantidade_reservas': quantidade_reservas,
        'soma_total_valores': soma_total_valores,
        'reserva_mais_cara': reserva_mais_cara,
        'reserva_mais_longa': reserva_mais_longa,
        'dias_mais_longa': dias_mais_longa,
        'quartos_reservados': quartos_reservados
    }
