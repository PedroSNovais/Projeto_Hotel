"""
Sistema de Gerenciamento de Reservas de Hotel
Hotel Flor de Lótus

Módulo principal que coordena a execução do sistema.
"""

from arquivo import carregar_reservas
from interface import (
    exibir_menu,
    exibir_todas_reservas,
    consultar_reserva_por_nome,
    exibir_estatisticas_gerais
)
from reserva import criar_reserva, cancelar_reserva
from utils import validar_entrada_inteira


def executar_sistema():
    """
    Função principal que executa o loop do sistema de reservas.
    """
    # Carrega as reservas existentes
    reservas = carregar_reservas()
    
    print("\n" + "="*60)
    print("BEM-VINDO AO SISTEMA DE RESERVAS")
    print("HOTEL FLOR DE LÓTUS")
    print("="*60 + "\n")
    
    
    while True:
        exibir_menu()
        opcao = validar_entrada_inteira(
            'Digite o código da opção desejada: ',
            minimo=1,
            maximo=6
        )
        
        if opcao == 1:
            criar_reserva(reservas)
            
        elif opcao == 2:
            consultar_reserva_por_nome(reservas)
            
        elif opcao == 3:
            exibir_todas_reservas(reservas)
            
        elif opcao == 4:
            cancelar_reserva(reservas)
            
        elif opcao == 5:
            exibir_estatisticas_gerais(reservas)
            
        elif opcao == 6:
            print("\n" + "="*60)
            print("ENCERRANDO O SISTEMA")
            print("Obrigado por utilizar o Hotel Flor de Lótus!")
            print("="*60 + "\n")

            break
        
        # Pausa para o usuário visualizar a informação
        if opcao != 6:
            input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    executar_sistema()
