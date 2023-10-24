from datetime import datetime

# Mapeamento das abreviações de meses para números
meses = {
    "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
    "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12
}

def converter_data(data_original, empresa):
    if empresa == 'Decolar':
      # Dividindo a data original em partes
      partes = data_original.split()

      # Extrair o dia, mês e ano da data original
      dia = int(partes[1])
      mes_abreviado = partes[2].lower().replace('.', '')
      mes = meses.get(mes_abreviado)

      if mes is None:
          return "Mês não reconhecido"
      
      ano = int(partes[3])

      # Formatar a data no estilo "dd/mm/yy"
      data_formatada = datetime(year=ano, month=mes, day=dia).strftime("%d/%m/%y")

      return data_formatada
    else:
      # Obter o ano atual
      ano_atual = datetime.now().year

      # Data no formato original
      data_original = "qua, 1 de Nov"

      # Dividir a data em partes
      partes = data_original.split(' ')

      # Extrair o dia, mês e ano
      dia = partes[1]
      mes = partes[3].lower()
      
      mes_numero = meses[mes]

      # Formatar a data no estilo 'dd/mm/yy'
      data_formatada = f"{dia}/{mes_numero:02}/{ano_atual % 100:02}"

      return data_formatada