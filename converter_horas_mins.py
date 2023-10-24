def converter_horas_para_minutos(padrao_horas):
    # Dividir o padrão de horas em horas e minutos
    partes = padrao_horas.split()
    horas = 0
    minutos = 0

    i = 0
    while i < len(partes):
        parte = partes[i]
        if parte == 'h':
            horas = 0  # Quando não há um valor numérico de horas, definimos como zero.
        elif parte.endswith('h'):
            horas = int(parte[:-1])
        elif parte.endswith('min'):
            minutos = int(parte[:-3])
        i += 1

    # Calcular o total de minutos
    total_minutos = (horas * 60) + minutos

    return total_minutos

# # Exemplo de uso da função
# padrao_horas = "0h 55min"
# total_minutos = converter_horas_para_minutos(padrao_horas)
# print("Total de minutos:", total_minutos)