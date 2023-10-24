import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from converter_data import converter_data
from converter_horas_mins import converter_horas_para_minutos
from inserir_banco import inserir_voos_bd

def scraperDecolar(url):
  driver = webdriver.Chrome()
  driver.get(url)
  # Delay em segundos para aguardar a página carregar
  time.sleep(20)

  # Iniciarlizar dicionário
  dic_voos = {'empresa': [], 'companhia_area': [], 'preco_total': [], 'taxa_embarque': [], 'taxa_servico': [], 'tempo_voo_min': [], 'data_hora_ida': [], 'data_hora_volta': []}

  # Carregar pagina até botão de carregar mais voos aparecer
  max_tentativas = 5
  intervalo_espera = 5 # 2 segundos
  elemento_botao = '//*[@id="clusters"]/div/a' 
  
  for _ in range(max_tentativas):
    try:
      botao_carregar_mais = driver.find_element(By.XPATH, elemento_botao)      
      break  # Botão encontrado, saia do loop
    except NoSuchElementException:
        # Botão não encontrado, role para baixo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(intervalo_espera)
  
  # Clicar no botão Carregar Mais Voos
  time.sleep(5)
  driver.execute_script("arguments[0].click();", botao_carregar_mais)
  time.sleep(15) # Aguardar dados carregarem

  #Loop para as melhores ofertas
  for i in range(1, 100):
    elemento_pai = f'//*[@id="clusters"]/span[{i}]/div/span/cluster/div/div'
    
    try:
      elemento_completo = driver.find_element(By.XPATH, elemento_pai)
      
      texto_card = elemento_completo.text
      
      # Companhia area
      companhia_area = re.search(r'Bagagem\n(.+)', texto_card).group(1)
      
      # Preço total
      preco_total = re.search(r'Preço final\n(.+)', texto_card).group(1).replace('R$', '')
      
      # Taxa de serviço
      taxa_servico = re.search(r'Impostos, taxas e encargos\n(.+)', texto_card).group(1).replace('R$', '')
      
      # Tempo de Voo em minutos
      tempo_voo_horas = re.search(r'(\d+h \d+m)', texto_card).group(0)
      tempo_voo_min = converter_horas_para_minutos(tempo_voo_horas)
    
      
      horas_encontradas = re.findall(r'\d+:\d+', texto_card)
      hora_ida = horas_encontradas[0]
      hora_volta = horas_encontradas[2]
      print(hora_ida, hora_volta)
      
      # Data ida
      data_ida = re.search(r'(\w+\. \d+ \w+\. \d+)', texto_card).group(0)
      data_ida_formatada = converter_data(data_ida, empresa='DECOLAR')
      # Data hora ida
      data_hora_ida = data_ida_formatada + ' ' + hora_ida
      
      #Data volta
      data_volta = re.search(r'VOLTA\n(\w+\. \d+ \w+\. \d+)', texto_card).group(1)
      data_volta_formatada = converter_data(data_volta, empresa='DECOLAR')
      # Data hora volta
      data_hora_volta = data_volta_formatada + ' ' + hora_volta
      
      dic_voos['empresa'].append('Decolar')
      dic_voos['companhia_area'].append(companhia_area)
      dic_voos['preco_total'].append(preco_total)
      dic_voos['taxa_embarque'].append('0')
      dic_voos['taxa_servico'].append(taxa_servico)
      dic_voos['tempo_voo_min'].append(tempo_voo_min)
      dic_voos['data_hora_ida'].append(data_hora_ida)
      dic_voos['data_hora_volta'].append(data_hora_volta)      
      
      print("Voo: ", i, " Empresa: Decolar ", " Companhia area: ", companhia_area, " Preco Total: ", preco_total, " Tempo Voo Min: ", tempo_voo_min, " Taxa Servico: ", taxa_servico, " Data hora ida: ", data_hora_ida, " Data hora volta: ", data_hora_volta)
      
    except NoSuchElementException:
      print(elemento_pai)
      continue
    
  for chave, valor in dic_voos.items():
      print(chave, ":", valor)
  
  # Chamada da função que vai inserir os dados no banco
  inserir_voos_bd(dic_voos)
  
  # Fechar Chrome
  driver.quit()
  
# #Testar script
# url = 'https://www.decolar.com/shop/flights/results/roundtrip/SAO/RIO/2023-11-01/2023-11-04/1/0/0?from=SB&di=1-0&reSearch=true'
# scraperDecolar(url)