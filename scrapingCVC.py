import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from converter_data import converter_data
from inserir_banco import inserir_voos_bd
from converter_horas_mins import converter_horas_para_minutos

def scraperCVC(url):
  driver = webdriver.Chrome()
  driver.get(url)
  html_content = driver.page_source
  # Delay em segundos para aguardar a página carregar
  time.sleep(20)

  # Iniciarlizar dicionário
  dic_voos = {'empresa': [], 'companhia_area': [], 'preco_total': [], 'taxa_embarque': [], 'taxa_servico': [], 'tempo_voo_min': [], 'data_hora_ida': [], 'data_hora_volta': []}

  # Localizar a quantidade de resultados encontrados
  elemento = driver.find_element(By.XPATH, '//*[@id="totalPricegroups"]')
  voos_encontrados = elemento.text
  # Regex para tratar a string e retirar o numero de voos
  qtd_voos = re.search(r'\d+', voos_encontrados).group()
  print("Quantidade de resultados encontrado: ", qtd_voos)

  # Loop para as melhores ofertas
  for i in range(2, int(qtd_voos)+1):
    # Tratativa para as duas primeiras divs da tela
    if i < 4:
      elemento_pai = f'//*[@id="cards-list"]/div[{i}]/div[2]'
    elif i >= 5:
      elemento_pai = f'//*[@id="cards-list"]/div[{i}]/div'
    
    if i == 23:
      # Role para baixo para carregar mais resultados
      # inicialmente só aparece 22 resultados na página
      elemento = driver.find_element(By.XPATH, elemento_pai)
      # Scroll da pagina até o final
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
      # Delay para aguardar resultados carregarem
      time.sleep(10)
        
    try:
      elemento_completo = driver.find_element(By.XPATH, elemento_pai)
      
      # Companhia Area
      path = f'{elemento_pai}/div[1]/div[1]/div/div[1]/div[1]/h6/span/span'
      elemento = driver.find_element(By.XPATH, path)
      companhia_area = elemento.text.replace('(', '').replace(')', '')
      
      # Preco Total
      path = f'{elemento_pai}/div[2]/div[1]/div[1]/div[2]/div/p/h5'
      elemento = driver.find_element(By.XPATH, path)
      preco_total = elemento.text

      path_expandir = f'{elemento_pai}/div[2]/div[1]/div[1]/div[2]/div/p'
      # Expandir preco para carregar taxa de embarque e servico
      elemento_expandir = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path_expandir)))
      driver.execute_script("arguments[0].click();", elemento_expandir)
      path_aguardar_elemento = f'{elemento_pai}/div[2]/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/span[2]'
      WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, path_aguardar_elemento)))
      
      # Taxa de embarque
      path = f'{elemento_pai}/div[2]/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/span[2]'
      elemento = driver.find_element(By.XPATH, path)
      taxa_embarque = elemento.text.replace('R$', '').strip()
      
      # Taxa de servico
      path = f'{elemento_pai}/div[2]/div[1]/div[1]/div[2]/div/div/div/div/div/div[3]/span[2]'
      elemento = driver.find_element(By.XPATH, path)
      taxa_servico = elemento.text.replace('R$', '').strip()
      
      texto = elemento_completo.text
      
      # # Tempo de voo em minutos
      # Use regex para encontrar o tempo no texto
      padrao = r'Total: (\d+h \d+min)'
      correspondencias = re.search(padrao, texto)

      if correspondencias:
          tempo_voo_horas = correspondencias.group(1)
      else:
          print("Tempo não encontrado na string.")
      # Conveter tempo de voo de horas para minutos
      tempo_voo_min = converter_horas_para_minutos(tempo_voo_horas)
      
      # Hora ida e hora volta
      horas_encontradas = re.findall(r'\d{1,2}:\d{2}', texto)
      # Acesse a primeira e terceira horas encontradas
      hora_ida = horas_encontradas[0]
      hora_volta = horas_encontradas[2]
      
      ## Data hora ida
      # Data ida
      path = f'{elemento_pai}/div[1]/div[1]/div/div[1]/div[2]/p[1]'
      elemento = driver.find_element(By.XPATH, path)
      data_ida = elemento.text
      data_hora_ida = converter_data(data_ida, empresa='CVC') + ' ' + hora_ida
      
      # Data hora volta
      path = f'{elemento_pai}/div[1]/div[2]/div/div[1]/div[2]/p[1]'
      elemento = driver.find_element(By.XPATH, path)
      data_volta = elemento.text
      data_hora_volta = converter_data(data_volta, empresa='CVC')  + ' ' + hora_volta
      
      dic_voos['empresa'].append('CVC')
      dic_voos['companhia_area'].append(companhia_area)
      dic_voos['preco_total'].append(preco_total)
      dic_voos['taxa_embarque'].append(taxa_embarque)
      dic_voos['taxa_servico'].append(taxa_servico)
      dic_voos['tempo_voo_min'].append(tempo_voo_min)
      dic_voos['data_hora_ida'].append(data_hora_ida)
      dic_voos['data_hora_volta'].append(data_hora_volta)
      
      print("Voo: ", i, " Empresa: CVC ", " Companhia area: ", companhia_area, " Preco Total: ", preco_total, " Tempo Voo Min: ", tempo_voo_min, " Taxa Embarque: ", taxa_embarque," Taxa Servico: ", taxa_servico, " Data hora ida: ", data_hora_ida, " Data hora volta: ", data_hora_volta)
      
    except NoSuchElementException:
      continue

  for chave, valor in dic_voos.items():
    print(chave, ":", valor)
    
  # Chamada da função que vai inserir os dados no banco
  inserir_voos_bd(dic_voos)
  
  # Fechar Chrome
  driver.quit()

# #Testar script
# url = 'https://www.cvc.com.br/passagens/v2/search/SAO/RIO?Date1=2023-11-01&Date2=2023-11-04&ADT=1&CHD=0&INF=0&CLA=all&STO=PACKAGE&MCO1=S%C3%A3o%20Paulo%20-%20SP%20,%20Brasil&MCD1=Rio%20de%20Janeiro%20-%20RJ%20,%20Brasil'
# scraperCVC(url)