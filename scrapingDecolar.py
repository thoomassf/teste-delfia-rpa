import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
from dotenv import load_dotenv

from converter_data import converter_data
from conveter_horas_mins import converter_horas_para_minutos
from inserir_banco import inserir_voos_bd

def scraperDecolar(url):
  driver = webdriver.Chrome()
  driver.get(url)
  # Delay em segundos para aguardar a página carregar
  time.sleep(20)

  # Iniciarlizar dicionário
  dic_voos = {'empresa': [], 'companhia_area': [], 'preco_total': [], 'taxa_embarque': [], 'taxa_servico': [], 'tempo_voo_min': [], 'data_hora_ida': [], 'data_hora_volta': []}

  # Localizar a quantidade de resultados encontrados
  # elemento = driver.find_element(By.XPATH, '//*[@id="filter-baggage"]/li/ul/div/checkbox-filter/checkbox-filter-item[1]/li/span/span[2]')
  # print(elemento)
  # qtd_voos = elemento.text.strip()
  # print("Quantidade de resultados encontrado: ", qtd_voos)
  
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
  
  # Extrair os dados do voo enquanto existir dados para carregar
  #while True:
  try:
    # Clicar no botão Carregar Mais Voos
    time.sleep(5)
    driver.execute_script("arguments[0].click();", botao_carregar_mais)
    #botao_carregar_mais.click()
    time.sleep(15) # Aguardar dados carregarem
  except NoSuchElementException:
    print("cliquei no botao saindo do try")
    # Botão Carregar Mais não está mais visivel, sair do loop
    #break
    
  # x = f'//*[@id="clusters"]/span[1]/div/span/cluster/div/div'
  # y = driver.find_element(By.XPATH, x)
  # print(y.text)

  #Loop para as melhores ofertas
  for i in range(1, 40):
    #elemento_pai = f'//*[@id="clusters"]/span[{i}]/div/span/cluster/div/div/div[1]/div/span/div/div[2]'
    elemento_pai = f'//*[@id="clusters"]/span[{i}]/div/span/cluster/div/div'
    # elemento = driver.find_element(By.XPATH, elemento_pai)
    # print(elemento.text)
    
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
      
      # Data ida
      data_ida = re.search(r'(\w+\. \d+ \w+\. \d+)', texto_card).group(0)
      data_ida_formatada = converter_data(data_ida, empresa='DECOLAR')
      # Horario ida
      horario_ida = re.search(r'(\d+:\d+)', texto_card).group(1)
      # Data hora ida
      data_hora_ida = data_ida_formatada + ' ' + horario_ida
      
      # Data ida
      data_volta = re.search(r'VOLTA\n(\w+\. \d+ \w+\. \d+)', texto_card).group(1)
      data_volta_formatada = converter_data(data_volta, empresa='DECOLAR')
      # Horario ida
      horario_ida = re.search(r'(\d+:\d+)', texto_card).group(1)
      # Data hora ida
      data_hora_volta = data_volta_formatada + ' ' + horario_ida
      # Data Hora Ida
      
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
  
  server = 'localhost,1433'  # Endereço do servidor e porta
  database = 'DB_Voos'  # Nome do banco de dados
  username = 'sa'  # Nome de usuário 'sa' (admin)
  password = 'Senha123#'  # Senha definida durante a criação do contêiner SQL Server
  # Carregar as váriaveis em ambiente do arquivo .env
  # load_dotenv()
  # # Agora você pode acessar as variáveis de ambiente
  # db_host = os.getenv("DB_HOST")
  # db_port = os.getenv("DB_PORT")
  # db_user = os.getenv("DB_USER")
  # db_password = os.getenv("DB_PASSWORD")
  # Chamer métoto que insere os dados no banco
  inserir_voos_bd(dic_voos, server, database, username, password)
  
  # Fechar Chrome
  driver.quit()
  
url = 'https://www.decolar.com/shop/flights/results/roundtrip/SAO/RIO/2023-11-01/2023-11-04/1/0/0?from=SB&di=1-0&reSearch=true'
scraperDecolar(url)