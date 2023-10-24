def converter_horas_para_minutos(padrao_horas):
    # Dividir o padrão de horas em horas e minutos
    partes = padrao_horas.split()
    horas = 0
    minutos = 0

    for parte in partes:
        if parte.endswith('h'):
            horas = int(parte[:-1])
        elif parte.endswith('m'):
            minutos = int(parte[:-1])

    # Calcular o total de minutos
    total_minutos = (horas * 60) + minutos

    return total_minutos

# Exemplo de uso da função
# padrao_horas = "1h"
# total_minutos = converter_horas_para_minutos(padrao_horas)
# print("Total de minutos:", total_minutos)