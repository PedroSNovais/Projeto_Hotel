from datetime import datetime
import os
import pickle
from config import *
from arquivo import *
    
reservas = carregar_reservas()

quartos_quantidade = QUARTOS_QUANTIDADE
quartos_valor = QUARTOS_VALOR
tipos = TIPOS_QUARTOS

def main():
    
    cod = 0
    while cod != 6:
        exibir_menu() 
        try:
            cod = int(input('DIGITE O CÓDIGO DO QUE DESEJA: '))
        except ValueError:
            print('ERRO! TENTE NOVAMENTE')
            continue
        match cod:
            case 1:
                fazer_reserva()
                continue
            case 2:
                consultar_reserva()
                continue
            case 3:
                exibir_reservas()
                continue
            case 4:
                cancelar_reserva()
                continue
            case 5:
                exibir_estatisticas()
                continue
            case defalt:
                print('codigo inexistente!!')
                continue
    print("Fim do programa")
    
def exibir_menu():
    menu = f'''
    {'-=' * 30}
    HOTEL FLOR DE LOTUS
    {'-=' * 30}
    1 - Fazer nova reserva
    2 - Consutar reserva por responsavel
    3 - Listar reservas existentes
    4 - Cancelar reserva
    5 - Estatísticas gerais
    6 - Sair
    {'-=' * 30}
    '''
    print(menu)    

def definir_valor_reserva_reais(reserva_para_analise: dict) -> int:
    
    valor_diaria = quartos_valor[reserva_para_analise['TIPO_QUARTO']]
    tempo_estadia = (reserva_para_analise['CHECKOUT'] - reserva_para_analise['CHECKIN']).days
    
    valor_reserva = valor_diaria * tempo_estadia * reserva_para_analise['QUANTIDADE_QUARTOS']

    return valor_reserva

def receber_informacoes():
    limpar_terminal()
    while True:
        print('--' * 30)
        responsavel = str(input("Digite o nome do responsavel pela reserva: ").strip().capitalize())
        data_chekIn_str = str(input("Digite a data de check in: (dd/mm/aaaa) "))
        data_chekOut_str = str(input("Digite a data de check out: (dd/mm/aaaa) "))
        tipo_quarto = str(input("Digite o tipo de quarto: ").strip().lower())
        quantidade_quartos = int(input("Digite a quantidade de quartos: "))
        
        if tipo_quarto not in tipos:
            print("Erro! Digite um tipo de quarto valido.")
            continue

        try: 
            data_chekIn = datetime.strptime(data_chekIn_str, "%d/%m/%Y")
            data_chekOut = datetime.strptime(data_chekOut_str, "%d/%m/%Y")
        except ValueError:
            print("Ocorreu um erro ao verificar as datas")
            print("Digite datas validas!")
            continue
        try:
            dias_reserva = data_chekOut - data_chekIn
            dias_reserva = dias_reserva.days
            if dias_reserva < 0:
                raise ValueError("Erro! Digite datas validas!")
        except ValueError:
            print("Erro! Digite datas validas!")
            continue
        break
    reserva_atual = {'NOME': responsavel, 'CHECKIN': data_chekIn ,'CHECKOUT': data_chekOut, 'TIPO_QUARTO': tipo_quarto, 'QUANTIDADE_QUARTOS': quantidade_quartos}
    reserva_atual.update({"HASH": -hash(str(reserva_atual))})
    reserva_atual.update({"VALOR": definir_valor_reserva_reais(reserva_atual)})
    return reserva_atual

def fazer_reserva():
    
    reserva_atual = receber_informacoes()
    validacao: bool = validar_reserva(reserva_atual)
    
    if validacao:
        reservas.append(reserva_atual)
        salvar_reservas(reservas)
        print('RESERVA REALIZADA COM SUCESSO !!')
    else:
        print('NÃO FOI POSSIVEL REALIZAR ESSA RESERVA !!')
        print("ESCOLHA OUTRO TIPO/QUANTIDADE DE QUARTOS OU TROQUE AS DATAS")

def validar_reserva(reserva_para_analise: dict) -> bool:
    quartos_ocupados = 0
    for reserva in reservas:
        if reserva_para_analise['TIPO_QUARTO'] == reserva['TIPO_QUARTO']:
            if reserva_para_analise['CHECKIN'] < reserva['CHECKOUT'] and reserva_para_analise['CHECKOUT'] > reserva['CHECKIN']:
                quartos_ocupados += reserva['QUANTIDADE_QUARTOS']

    quartos_disponiveis = quartos_quantidade[reserva_para_analise['TIPO_QUARTO']] - quartos_ocupados

    if quartos_disponiveis < reserva_para_analise['QUANTIDADE_QUARTOS']:
        return False
    else:
        return True

def exibir_reservas():
    limpar_terminal()
    print("função de exibir TODAS as reservas")
    for reserva in reservas:
        for chave, valor in reserva.items():
            print(f"{chave} --> {valor}")

        print('--' * 30)
        
def consultar_reserva():
    limpar_terminal()
    print("função de exibir reserva especfica")
    nome_consulta = str(input("Digite o nome do responsavel da reserva: ").strip().capitalize())
    cont = 0
    
    for reserva in reservas:
        if reserva['NOME'] == nome_consulta:
            cont += 1
            for chave, valor in reserva.items():
                print(f"{chave} --> {valor}")
            print('--' * 30)

    if cont == 0:
        print('Não foram encontradas reservas para essa pessoa!')
        print('Verifique o nome ou colsulte a lista completa de reservas')

def cancelar_reserva():
    hash_ = int(input("Digite o codigo (HASH) da reserva: "))
    for indice ,reserva in enumerate(reservas):
        if reserva["HASH"] == hash_:
            if reserva['CHECKOUT'] < datetime.today():
                print('ESSA RESERVA NÃO PODE SER CANCELADA.')
            else:
                reservas.pop(indice)
                salvar_reservas(reservas)
                print("RESERVA DELETADA COM SUCESSO!!")       

def calcular_estatisticas():

    
    if reservas != []:
        quantidade_reservas_realizadas = len(reservas)
        reserva_mais_cara = reservas[0]
        reserva_mais_longa = reservas[0]
        quantidade_quartos_reservados = {"standard": 0, "premium": 0, "luxo": 0}
        
        soma_total_valor_reservas = 0 
        for reserva in reservas:
            # Calculando a reserva mais longa
            reserva_mais_longa_dias = (reserva_mais_longa['CHECKOUT'] - reserva_mais_longa['CHECKIN']).days
            if (reserva['CHECKOUT'] - reserva['CHECKIN']).days > reserva_mais_longa_dias:
                reserva_mais_longa = reserva
            
            # Calculando a reserva mais cara
            if (reserva["VALOR"] > reserva_mais_cara["VALOR"]):
                reserva_mais_cara = reserva

            # Calculando a quanti. quartos reservados
            quantidade_quartos_reservados[reserva["TIPO_QUARTO"]] += reserva["QUANTIDADE_QUARTOS"]

            # Calculando a soma total dos valores das reservas
            soma_total_valor_reservas += reserva["VALOR"]


            



            
        return (quantidade_reservas_realizadas, soma_total_valor_reservas ,reserva_mais_cara, reserva_mais_longa, quantidade_quartos_reservados)

            
        
    else:
        print("Não há reservas feitas.")

def exibir_estatisticas():
    quantidade_reservas_realizadas, soma_total_valor_reservas ,reserva_mais_cara,reserva_mais_longa, quantidade_quartos_reservados = calcular_estatisticas()

    estatisticas = f'''

    QUANTIDADE DE RESERVAS REALIZADAS: {quantidade_reservas_realizadas};
    SOMA TOTAL DO VALOR DAS RESERVAS: {soma_total_valor_reservas};
   
    A RESERVA MAIS CARA ESTÁ NO NOME DE {reserva_mais_cara["NOME"]}
    E CUSTOU R${reserva_mais_cara["VALOR"]};
    
    A RESERVA MAIS LONGA ESTÁ NO NOME DE {reserva_mais_longa["NOME"]}
    E POSSUI {(reserva_mais_longa["CHECKOUT"]-reserva_mais_longa["CHECKIN"]).days} DIAS;
    
    TOTAL DE QUARTOS RESERVADOS:
        STANDARD: {quantidade_quartos_reservados["standard"]};
        PREMIUM: {quantidade_quartos_reservados["premium"]};
        LUXO: {quantidade_quartos_reservados["luxo"]};
    '''
    print(estatisticas)

def limpar_terminal():
    """Limpa a tela do terminal de forma compativel com o Sistema Operacional."""
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")


if __name__ == "__main__": main()