from scrapingDecolar import scraperDecolar
from scrapingCVC import scraperCVC

class Main:
  origem = 'SAO'
  destino = 'RIO'
  data_ida = '2023-11-01'
  data_volta = '2023-11-04'
  
  url = f"https://www.decolar.com/shop/flights/results/roundtrip/{origem}/{destino}/{data_ida}/{data_volta}/1/0/0?from=SB&di=1-0&reSearch=true"
  scraperDecolar(url)
  
  url = f"https://www.cvc.com.br/passagens/v2/search/{origem}/{destino}?Date1={data_ida}&Date2={data_volta}&ADT=1&CHD=0&INF=0&CLA=all&STO=PACKAGE&MCO1=S%C3%A3o%20Paulo%20-%20SP%20,%20Brasil&MCD1=Rio%20de%20Janeiro%20-%20RJ%20,%20Brasil"
  scraperCVC(url)