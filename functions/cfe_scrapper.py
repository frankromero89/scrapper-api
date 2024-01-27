import time
import os
from dotenv import load_dotenv
import logging
import boto3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()
chrome_options = Options()

chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("prefs",{"download.default_directory" : os.environ['DOWNLOAD_PATH']})

# s3 = boto3.resource('s3')

# for bucket in s3.buckets.all():
#     print(bucket.name)

def execute_scrapper(username: str, key: str, service: str):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

    url_login = 'https://app.cfe.mx/Aplicaciones/CCFE/MiEspacio/Login.aspx'

    driver.get(url_login)

    # Iniciar sesión en el sitio de CFE
    driver.find_element(By.NAME, 'ctl00$MainContent$txtUsuario').send_keys(username)
    driver.find_element(By.NAME, 'ctl00$MainContent$txtPassword').send_keys(key)
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit" i]').click()

    # Preparar el sitio con el número de usuario de CFE
    driver.find_element(By.LINK_TEXT, 'Inicio Consultar Recibo').click()

    # Ir a la sección de "Otras Facturas"
    driver.find_element(By.ID, 'ctl00_MainContent_GVHistorial_ctl02_hplMasFacturaciones').click()

    # Ingresar al número de servicio
    us = Select(driver.find_element(By.NAME, 'ctl00$MainContent$ddlServicios'))
    us.select_by_value(service)

    # Descargar la tabla de "Otras Facturas"
    # statements = driver.find_elements(By.XPATH, "//*[@id='ctl00_MainContent_gvFacturasUsuario']/tbody/tr")
    row = len(driver.find_elements(By.XPATH, "//*[@id='ctl00_MainContent_gvFacturasUsuario']/tbody/tr"))

    for n in range(2, row):
        try:
            if n < 10:
                driver.find_element(By.ID, f'ctl00_MainContent_gvFacturasUsuario_ctl0{n}_lnkDescargaXML').click()
            else:
                driver.find_element(By.ID, f'ctl00_MainContent_gvFacturasUsuario_ctl{n}_lnkDescargaXML').click()
            print(f'Downloaded file: {n}')
        except UnexpectedAlertPresentException:
            print(f'Error with file: {n}')
            alert_obj = driver.switch_to.alert
            alert_obj.accept()
            pass

    time.sleep(10)

    driver.quit()

    return {'success': True}

# if __name__ == '__main__': 
#     print(execute_scrapper()) 