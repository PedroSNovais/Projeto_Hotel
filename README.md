# Sistema de Gerenciamento de Reservas - Hotel Flor de Lótus

Sistema completo para gerenciamento de reservas de hotel, desenvolvido em Python seguindo boas práticas de programação estruturada (sem POO).

## Funcionalidades

1. **Fazer Nova Reserva**
   - Cadastro de responsável
   - Seleção de datas (check-in e check-out)
   - Escolha de tipo de quarto (standard, premium, luxo)
   - Definição de quantidade de quartos
   - Validação automática de disponibilidade
   - Cálculo automático do valor total

2. **Consultar Reserva por Responsável**
   - Busca por nome do responsável
   - Exibição de todas as reservas encontradas

3. **Listar Reservas Existentes**
   - Visualização de todas as reservas cadastradas
   - Informações completas de cada reserva

4. **Cancelar Reserva**
   - Cancelamento por código hash
   - Validação de período (não permite cancelar reservas passadas)

5. **Estatísticas Gerais**
   - Quantidade total de reservas
   - Valor total arrecadado
   - Reserva mais cara
   - Reserva mais longa
   - Quantidade de quartos reservados por tipo

## Estrutura do Projeto

```
hotel_refatorado/
├── main.py           # Módulo principal - coordena o sistema
├── config.py         # Configurações e constantes
├── arquivo.py        # Persistência de dados (pickle)
├── utils.py          # Funções utilitárias gerais
├── calculo.py        # Cálculos e validações
├── interface.py      # Interface com usuário
├── reserva.py        # Gerenciamento de reservas
├── README.md         # Este arquivo
├── MELHORIAS.md      # Documentação das melhorias aplicadas
└── data/             # Diretório criado automaticamente
    └── reservas.pkl  # Arquivo de dados das reservas
```

## Requisitos

- Python 3.11 ou superior
- Módulos padrão (datetime, os, pickle)

## Como Executar

```bash
cd hotel_refatorado
python3.11 main.py
```

## Configurações

As configurações do hotel podem ser alteradas no arquivo `config.py`:

```python
# Quantidade de quartos disponíveis por tipo
QUARTOS_QUANTIDADE = {
    "standard": 10,
    "premium": 5,
    "luxo": 3
}

# Valor da diária por tipo de quarto
QUARTOS_VALOR = {
    "standard": 100.00,
    "premium": 180.00,
    "luxo": 250.00
}
```

## Formato de Dados

### Entrada de Datas
- Formato: `dd/mm/aaaa`
- Exemplo: `25/12/2025`

### Tipos de Quartos
- `standard`: Quarto padrão
- `premium`: Quarto premium
- `luxo`: Quarto de luxo

### Código da Reserva
- Gerado automaticamente como hash único
- Usado para consulta e cancelamento

## Validações Implementadas

1. **Datas:**
   - Check-out deve ser posterior ao check-in
   - Formato correto (dd/mm/aaaa)

2. **Tipo de Quarto:**
   - Deve ser um dos tipos válidos (standard, premium, luxo)

3. **Quantidade de Quartos:**
   - Deve ser número inteiro positivo
   - Deve haver disponibilidade no período

4. **Disponibilidade:**
   - Verifica sobreposição de datas
   - Calcula quartos ocupados por tipo
   - Valida se há quartos suficientes

5. **Cancelamento:**
   - Não permite cancelar reservas já concluídas
   - Valida existência do código

## Persistência de Dados

- Os dados são salvos automaticamente em arquivo pickle
- Localização: `data/reservas.pkl`
- Carregamento automático ao iniciar o sistema
- Salvamento automático após cada operação

## Boas Práticas Aplicadas

✅ Separação de responsabilidades por módulo  
✅ Funções com propósito único  
✅ Nomenclatura consistente e descritiva  
✅ Documentação completa (docstrings)  
✅ Tratamento robusto de erros  
✅ Validação de entrada do usuário  
✅ Código DRY (Don't Repeat Yourself)  
✅ Eliminação de importações circulares  
✅ Uso de constantes centralizadas  
✅ Interface amigável e profissional  

## Exemplo de Uso

```
============================================================
BEM-VINDO AO SISTEMA DE RESERVAS
HOTEL FLOR DE LÓTUS
============================================================

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    HOTEL FLOR DE LÓTUS
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    1 - Fazer nova reserva
    2 - Consultar reserva por responsável
    3 - Listar reservas existentes
    4 - Cancelar reserva
    5 - Estatísticas gerais
    6 - Sair
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

Digite o código da opção desejada: 1

============================================================
NOVA RESERVA
============================================================

Nome do responsável pela reserva: João Silva
Data de check-in (dd/mm/aaaa): 01/12/2025
Data de check-out (dd/mm/aaaa): 05/12/2025

Tipos de quarto disponíveis: standard, premium, luxo
Tipo de quarto: premium
Quantidade de quartos: 2

============================================================
RESERVA REALIZADA COM SUCESSO!
============================================================
Código da Reserva: 1234567890
Responsável: João Silva
Período: 01/12/2025 a 05/12/2025
Valor Total: R$ 1.440,00
============================================================
```
