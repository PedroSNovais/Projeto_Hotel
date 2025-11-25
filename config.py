"""
Módulo de configuração centralizada do sistema de reservas.
Contém constantes e configurações globais.
"""

# Configurações de quartos
QUARTOS_QUANTIDADE = {
    "standard": 10,
    "premium": 5,
    "luxo": 3
}

QUARTOS_VALOR = {
    "standard": 100.00,
    "premium": 180.00,
    "luxo": 250.00
}

TIPOS_QUARTOS = ("standard", "premium", "luxo")

# Configurações de arquivo
DIRETORIO_DADOS = "data"
ARQUIVO_RESERVAS = "reservas.pkl"
