"""
Módulo de interface com o usuário.
Contém funções para exibição de informações e coleta de dados.
"""

from datetime import datetime
from Projeto_Hotel.config import TIPOS_QUARTOS
from utils import limpar_terminal, formatar_valor_monetario, validar_entrada_inteira
from calculo import calcular_estatisticas, calcular_dias_estadia

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
