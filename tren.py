import time
import winsound
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import telegram_send
#import pandas as pd


#Opciones de navegacion

options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-logging'])

executable_path = '/webdriver/chromedriver.exe'
browser = webdriver.Chrome(executable_path, options=options)

from selenium.webdriver.common.keys import Keys


#Inicializar el navegador

browser.get('https://webventas.sofse.gob.ar/index.php')

#Localidad Origen
time.sleep(0.5)
WebDriverWait(browser, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                       'input#origen-selectized')))\
    .send_keys('Cnel. Vidal', Keys.ENTER)

time.sleep(0.5)

#Localidad Destino
WebDriverWait(browser, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                       'input#destino-selectized')))\
    .send_keys('Buenos Aires', Keys.ENTER)

time.sleep(0.5)

#Moviendo en el calendario
browser.find_element(By.XPATH,'//*[@id="form_busqueda"]/div/div[4]/div[1]/div[1]/a/span')\
    .click()

#browser.find_element(By.XPATH,'//*[@id="datepicker-calendar-fecha_ida"]/div[1]/div[2]')\
  #  .click()

#Fecha de ida
browser.find_element(By.XPATH,'//*[@id="cell9-fecha_ida"]')\
    .click()

#Cant de adultos
browser.find_element(By.XPATH,'//*[@id="adulto"]/option[3]')\
    .click()

time.sleep(0.5)

#"Buscar servicios"
WebDriverWait(browser, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form_busqueda"]/div/div[7]/div/button')))\
            .click()

dia = "dia_no_disponible"
while dia == "dia_no_disponible":

    time.sleep(3)
    #Dia seleccionado
    dia = browser.find_element(By.XPATH,'//*[@id="calendario_ida"]/div[2]/div/div[4]/div').get_attribute("class")
    if dia == "dia_no_disponible":
    #Cond de corte
        time.sleep(3)
        #Si el elemento "Atencion" esta "displayed", aceptarlo y volver a buscar servicios
        element = browser.find_element(By.XPATH,'//*[@id="modal_alerta"]/div/div/div[3]/button[1]')
        if element.is_displayed() is True:
            element.click()
            WebDriverWait(browser, 5)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form_busqueda"]/div/div[7]/div/button')))\
                .click()
        #Sino, solo buscar servicios
        else:
            WebDriverWait(browser, 5)\
                .until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form_busqueda"]/div/div[7]/div/button')))\
                .click()

        #Excepciones
        
    #Si encuentra pasajes para dicha fecha, corta el bucle, envia mensaje a telegram y reproduce sonido
    else: 
        print("Pasajes encontrados!")
        telegram_send.send(messages=["Hay Pasajes disponibles wachin"])
        winsound.Beep(440, 1000)