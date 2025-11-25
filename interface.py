"""
Módulo de interface com o usuário.
Contém funções para exibição de informações e coleta de dados.
"""

from datetime import datetime
from config import TIPOS_QUARTOS
from utils import limpar_terminal, formatar_valor_monetario, validar_entrada_inteira
from calculo import calcular_estatisticas, calcular_dias_estadia


def exibir_menu():
    """
    Exibe o menu principal do sistema.
    """
    menu = f'''
    {'-=' * 30}
    HOTEL FLOR DE LÓTUS
    {'-=' * 30}
    1 - Fazer nova reserva
    2 - Consultar reserva por responsável
    3 - Listar reservas existentes
    4 - Cancelar reserva
    5 - Estatísticas gerais
    6 - Sair
    {'-=' * 30}
    '''
    print(menu)


def exibir_reserva(reserva):
    """
    Exibe os detalhes de uma reserva.
    
    Args:
        reserva (dict): Dicionário contendo os dados da reserva
    """
    print(f"Código da Reserva: {reserva['hash']}")
    print(f"Responsável: {reserva['nome']}")
    print(f"Check-in: {reserva['checkin'].strftime('%d/%m/%Y')}")
    print(f"Check-out: {reserva['checkout'].strftime('%d/%m/%Y')}")
    print(f"Tipo de Quarto: {reserva['tipo_quarto'].capitalize()}")
    print(f"Quantidade de Quartos: {reserva['quantidade_quartos']}")
    print(f"Valor Total: {formatar_valor_monetario(reserva['valor'])}")
    print('--' * 30)


def exibir_todas_reservas(reservas):
    """
    Exibe todas as reservas cadastradas.
    
    Args:
        reservas (list): Lista de reservas
    """
    limpar_terminal()
    
    if not reservas:
        print("Não há reservas cadastradas.")
        return
    
    print(f"\n{'='*60}")
    print(f"TODAS AS RESERVAS ({len(reservas)} encontrada(s))")
    print(f"{'='*60}\n")
    
    for reserva in reservas:
        exibir_reserva(reserva)


def consultar_reserva_por_nome(reservas):
    """
    Consulta e exibe reservas de um responsável específico.
    
    Args:
        reservas (list): Lista de reservas
    """
    limpar_terminal()
    print(f"\n{'='*60}")
    print("CONSULTAR RESERVA POR RESPONSÁVEL")
    print(f"{'='*60}\n")
    
    nome_consulta = input("Digite o nome do responsável da reserva: ").strip().capitalize()
    
    reservas_encontradas = [
        reserva for reserva in reservas 
        if reserva['nome'] == nome_consulta
    ]
    
    if reservas_encontradas:
        print(f"\n{len(reservas_encontradas)} reserva(s) encontrada(s) para {nome_consulta}:\n")
        for reserva in reservas_encontradas:
            exibir_reserva(reserva)
    else:
        print(f"\nNão foram encontradas reservas para '{nome_consulta}'.")
        print("Verifique o nome ou consulte a lista completa de reservas.")


def exibir_estatisticas_gerais(reservas):
    """
    Exibe estatísticas gerais sobre as reservas.
    
    Args:
        reservas (list): Lista de reservas
    """
    estatisticas = calcular_estatisticas(reservas)
    
    if not estatisticas:
        print("\nNão há reservas cadastradas para gerar estatísticas.")
        return
    
    print(f"\n{'='*60}")
    print("ESTATÍSTICAS GERAIS")
    print(f"{'='*60}\n")
    
    print(f"Quantidade de Reservas Realizadas: {estatisticas['quantidade_reservas']}")
    print(f"Valor Total de Todas as Reservas: {formatar_valor_monetario(estatisticas['soma_total_valores'])}")
    
    print(f"\nReserva Mais Cara:")
    print(f"  Responsável: {estatisticas['reserva_mais_cara']['nome']}")
    print(f"  Valor: {formatar_valor_monetario(estatisticas['reserva_mais_cara']['valor'])}")
    
    print(f"\nReserva Mais Longa:")
    print(f"  Responsável: {estatisticas['reserva_mais_longa']['nome']}")
    print(f"  Duração: {estatisticas['dias_mais_longa']} dia(s)")
    
    print(f"\nTotal de Quartos Reservados:")
    print(f"  Standard: {estatisticas['quartos_reservados']['standard']}")
    print(f"  Premium: {estatisticas['quartos_reservados']['premium']}")
    print(f"  Luxo: {estatisticas['quartos_reservados']['luxo']}")
    print()


def coletar_dados_reserva():
    """
    Coleta os dados necessários para criar uma nova reserva.
    
    Returns:
        dict: Dicionário com os dados da reserva ou None se houver erro
    """
    limpar_terminal()
    print(f"\n{'='*60}")
    print("NOVA RESERVA")
    print(f"{'='*60}\n")
    
    while True:
        # Coleta nome do responsável
        responsavel = input("Nome do responsável pela reserva: ").strip().capitalize()
        if not responsavel:
            print("Erro! O nome não pode estar vazio.")
            continue
        
        # Coleta datas
        try:
            data_checkin_str = input("Data de check-in (dd/mm/aaaa): ").strip()
            data_checkout_str = input("Data de check-out (dd/mm/aaaa): ").strip()
            
            data_checkin = datetime.strptime(data_checkin_str, "%d/%m/%Y")
            data_checkout = datetime.strptime(data_checkout_str, "%d/%m/%Y")
            
            # Valida datas
            dias_estadia = calcular_dias_estadia(data_checkin, data_checkout)
            if dias_estadia <= 0:
                print("Erro! A data de check-out deve ser posterior à data de check-in.")
                continue
                
        except ValueError:
            print("Erro! Digite datas válidas no formato dd/mm/aaaa.")
            continue
        
        # Coleta tipo de quarto
        print(f"\nTipos de quarto disponíveis: {', '.join(TIPOS_QUARTOS)}")
        tipo_quarto = input("Tipo de quarto: ").strip().lower()
        
        if tipo_quarto not in TIPOS_QUARTOS:
            print(f"Erro! Digite um tipo de quarto válido: {', '.join(TIPOS_QUARTOS)}")
            continue
        
        # Coleta quantidade de quartos
        quantidade_quartos = validar_entrada_inteira(
            "Quantidade de quartos: ",
            minimo=1
        )
        
        return {
            'nome': responsavel,
            'checkin': data_checkin,
            'checkout': data_checkout,
            'tipo_quarto': tipo_quarto,
            'quantidade_quartos': quantidade_quartos
        }
