import time
import os
import boto3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager


# def lambda_handler(event,context):
chrome_options = Options()

chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("prefs",{"download.default_directory" : "/Users/Pali/Desktop/wattcher/scrapper/statements",})

# s3 = boto3.resource('s3')

# for bucket in s3.buckets.all():
#     print(bucket.name)

def execute_scrapper():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

    url_login = 'https://app.cfe.mx/Aplicaciones/CCFE/MiEspacio/Login.aspx'

    driver.get(url_login)

    # Iniciar sesión en el sitio de CFE
    driver.find_element(By.NAME, 'ctl00$MainContent$txtUsuario').send_keys('adrianlivas')
    driver.find_element(By.NAME, 'ctl00$MainContent$txtPassword').send_keys('$8ihwdnklwG”(/IB')
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit" i]').click()

    # Preparar el sitio con el número de usuario de CFE
    driver.find_element(By.LINK_TEXT, 'Inicio Consultar Recibo').click()

    # Ir a la sección de "Otras Facturas"
    driver.find_element(By.ID, 'ctl00_MainContent_GVHistorial_ctl02_hplMasFacturaciones').click()

    # Ingresar al número de servicio
    us = Select(driver.find_element(By.NAME, 'ctl00$MainContent$ddlServicios'))
    us.select_by_value('779151001243')

    # Descargar la tabla de "Otras Facturas"
    statements = driver.find_elements(By.XPATH, "//*[@id='ctl00_MainContent_gvFacturasUsuario']/tbody/tr")
    row = len(driver.find_elements(By.XPATH, "//*[@id='ctl00_MainContent_gvFacturasUsuario']/tbody/tr"))

    for n in range(2, 4):
        print(f"******n: {n}")
        # name_file = driver.find_element(By.XPATH, f"//*[@id='ctl00_MainContent_gvFacturasUsuario']/tbody/tr[{n}]/td[{n}]").text
        # print(f'name_file: /app/WA-{name_file}.xml')
        try:
            if n < 10:
                driver.find_element(By.ID, f'ctl00_MainContent_gvFacturasUsuario_ctl0{n}_lnkDescargaXML').click()
            else:
                driver.find_element(By.ID, f'ctl00_MainContent_gvFacturasUsuario_ctl{n}_lnkDescargaXML').click()
        except UnexpectedAlertPresentException:
            # alert_obj = driver.switch_to.alert
            # alert_obj.accept()
            pass


    title = driver.title

    time.sleep(10)

    with open('/Users/Pali/Desktop/wattcher/scrapper/statements/WA-000058349451.xml', 'rb') as file:
        print(f"******file: {file}")

    driver.quit()

    return {'success': True}
