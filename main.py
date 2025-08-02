## librerias necesarias para el webscrapping ##
from random import random
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from datetime import datetime
import time, os 
from selenium.webdriver.common.alert import Alert
#############################################


# Creacion de cliente de automatizador #

def init_webdriver():
    
    #inicializar el servicio chrome automatizacion 
    service = Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()

    ### mostrando pantalla del funcionamiento ###
    option.add_argument("--window-size=1920,1080")

    ###sin mostrar pantalla ###
    #option.add_argument("--headless") 

    ### desabilita las extenciones (agiliza el funcionamiento) ###
    option.add_argument("--disable-extensions")

    ### desabilita el reconocimento de webdriver ###
    option.add_argument("--disable-blink-features-AutomationControlled")

    ### desactiva los parametros de automatizacion para hacer pasar selenium como humano ###
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)
    
    # Crear instancia del driver
    driver = Chrome(service=service, options=option)

    ## funcion que simula interfaz humana ##
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    
    print("WebDriver inicializado correctamente")
    return driver


def navigate_to_website(driver, url):
    try:
        driver.get(url)
        print(f"Navegando a: {url}")
        return True
    except Exception as e:
        print(f"Error al navegar a {url}: {e}")
        return False
###modal aleerts closer ####

def close_modal(webdriver):
    pages_tempt =  WebDriverWait(webdriver, 20).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[12]/div/div[2]/div"))
    )
    modal = bool(pages_tempt)
    print(modal)
    if modal:
        try:
            WebDriverWait(webdriver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div/div[2]/div/div/div/div/div/button"))
            ).click()
            
            print("close modal")
        except TimeoutException:
            print("Not modal to close")
    else:
        pass 


def filter_data(list_to_filter):
    list_to_filter = [element.text for element in list_to_filter]
    list_to_filter_parsed = []
    for item in list_to_filter:
        list_to_filter_parsed.extend(item.split('\n'))
    options = ['Free Shipping', 'On Sale', 'Recommended', 'Subscription', 'Drop-Shipped']
    filtered_list_to_filter = [item for item in list_to_filter_parsed if item  not in options]
    return filtered_list_to_filter
    



def command_click(webdriver, xpath):
    close_modal(webdriver)
    WebDriverWait(webdriver, 20).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()

def command_select_value(webdriver, xpath, selected_value):
    close_modal(webdriver)
    Select(WebDriverWait(webdriver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )).select_by_value(selected_value)


def command_get_data(webdriver, xpath):
    close_modal(webdriver)
    clear_data = []
    pages = get_pages(webdriver, xpath)
    while pages:
        try:
            data_tempt = WebDriverWait(webdriver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
            data = filter_data(data_tempt)
            clear_data.extend(data)
            print(f"Data captured: {len(clear_data)} items")
            print(clear_data)

            if len(webdriver.find_elements(By.XPATH, "/html/body/div[6]/div/div[1]/main/div/div[3]/div[3]/div/ul/li[3]/a/span")) > 0:
                command_click(webdriver, "/html/body/div[6]/div/div[1]/main/div/div[3]/div[3]/div/ul/li[3]/a/span")
            else:
                break
        except TimeoutException:
            print("Loading took too much time!")
            break
        time.sleep(20)  # Esperar a que se cargue la página

def get_pages(webdriver, xpath):
    close_modal(webdriver)
    pages_tempt =  WebDriverWait(webdriver, 20).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    return bool(pages_tempt)

#######starting scrapping#######

def all_products(driver):
    # try:
        pages_tempt = False
        while pages_tempt == False:
            time.sleep(20)
            try:
                pages_tempt =  WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[15]/div/div[2]/div/div/div/div"))
                )
                pages_tempt = bool(pages_tempt)
                print(f"Modal present: {pages_tempt}")
            except TimeoutException:
                break
            
        
        # command_click(driver, "/html/body/header/div/div[2]/div/nav/div/ul/li[2]/a")
        # command_click(driver, "/html/body/header/div/div[2]/div/nav/div/ul/li[2]/div/ul/li[2]/ul/li[1]/a")
       
        # command_select_value(driver, "/html/body/div[6]/div/div[1]/main/div/div[3]/div[1]/div/fieldset[2]/div/select", "100")
        # time .sleep(5)  # Esperar a que se cargue la página
        # #capture data per page 

        # data1 = command_get_data(driver, '/html/body/div[6]/div/div[1]/main/div/div[3]/div[2]')
        # print(data1)

        # pages = get_pages(driver, "/html/body/div[6]/div/div[1]/main/div/div[3]/div[3]/div/ul/li[3]/a/span")
        # WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div[2]/div/nav/div/ul/li[2]/a"))
        # ).click()

        # WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, "/html/body/header/div/div[2]/div/nav/div/ul/li[2]/div/ul/li[2]/ul/li[1]/a"))
        # ).click()

        
        # DropdedownAll= Select(WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH,"/html/body/div[6]/div/div[1]/main/div/div[3]/div[1]/div/fieldset[2]/div/select"))))
        # DropdedownAll.select_by_value("100")


        # time.sleep(5)  # Esperar a que se cargue la página
        # response_list = WebDriverWait(driver, 20).until(
        #      EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[6]/div/div[1]/main/div/div[3]/div[2]'))
        # )
        # filer_data(response_list)
        
    # except TimeoutException:
    #     print("Loading took too much time!")
    # except StaleElementReferenceException:
    #     print("Element is no longer attached to the DOM.")
    # except Exception as e:
    #     print(f"Error inesperado: {e}")


def close_driver(driver):
   
    try:
        driver.quit()
        print("WebDriver cerrado correctamente")
    except Exception as e:
        print(f"Error al cerrar el driver: {e}")


def main():
    driver = None
    
    try:
        # Inicializar el webdriver
        driver = init_webdriver()
        
        # Navegar al sitio web
        website = "https://prima-coffee.com/brew/coffee"
        if navigate_to_website(driver, website):
            # Ejecutar el scraping
            all_products(driver)
        
    except Exception as e:
        print(f"Error en el proceso principal: {e}")
    
    finally:
        # Cerrar el driver sin importar qué pase
        if driver:
            close_driver(driver)


# Ejecutar el programa principal
if __name__ == "__main__":
    main()


