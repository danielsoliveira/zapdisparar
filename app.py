#!pip install selenium
#!pip install webdriver-manager
#!pip install streamlit
import streamlit as st
import pandas as pd

from openpyxl import Workbook
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.core.utils import ChromeType

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import urllib
import time
import os
import random

st.title('ZapDisparar')
st.header('Lista de transmissão')
lista  = st.file_uploader("Selecione lista de contatos", type=["xlsx","xls"])
if lista is not None:
    tabela = pd.read_excel(lista)
    st.write(tabela)
botao = st.button('Enviar')
    
if botao and lista is not None:
    
    navegador = webdriver.Chrome(ChromeDriverManager(path = r".\chromedriver.exe").install())

    navegador.get("https://web.whatsapp.com")

    # esperar a tela do whatsapp carregar
    while len(navegador.find_elements(By.ID, 'side')) < 1: # -> lista for vazia -> que o elemento não existe ainda
        time.sleep(1)
    time.sleep(2) # só uma garantia
    
    for linha in tabela.index:
        # enviar uma mensagem para a pessoa
        nome = tabela.loc[linha, "nome"]
        mensagem = tabela.loc[linha, "mensagem"]
        imagem = tabela.loc[linha, "imagem"]
        telefone = tabela.loc[linha, "telefone"]
        
        texto = mensagem.replace("fulano", nome)
        texto = urllib.parse.quote(texto)

        # enviar a mensagem
        link = f"https://web.whatsapp.com/send?phone={telefone}&text={texto}"
        
        navegador.get(link)
        # esperar a tela do whatsapp carregar -> espera um elemento que só existe na tela já carregada aparecer
        while len(navegador.find_elements(By.ID, 'side')) < 1: # -> lista for vazia -> que o elemento não existe ainda
            time.sleep(1)
        time.sleep(2) # só uma garantia
        
        # você tem que verificar se o número é inválido
        if len(navegador.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')) < 1:
            
            # enviar a mensagem
            navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()
            
            if imagem != "N":
                caminho_completo = os.path.abspath(f"C:\zapdisparar\arquivos\{imagem}")
                navegador.find_element(By.XPATH, 
                                    '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span').click()
                navegador.find_element(By.XPATH, 
                                    '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input').send_keys(caminho_completo)
                time.sleep(3)
                navegador.find_element(By.XPATH, 
                                    '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span').click()
            
                time.sleep(1)
        time.sleep(random.randrange(5,8))
