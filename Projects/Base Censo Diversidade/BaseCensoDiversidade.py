
import time #Biblioteca para fazer pausas temporais

import pandas as pd #Biblioteca para manipular planilhas

import os #Bibliotecas para mover e manipular arquivos do computador
import os.path
import glob

import selenium #Biblioteca que vai fazer a automação
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


import chromedriver_autoinstaller #Bibilioteca para instalar o chromewebdriver

chromedriver_autoinstaller.install() #Instalando o chromewebdriver virtualmente


#Definindo algumas funções úteis para o script

def encontrar_ultimo_arquivo(pasta):
# Caminho para a pasta Downloads
    downloads_path = os.path.expanduser(pasta)

    # Lista de todos os arquivos na pasta Downloads
    all_files = glob.glob(os.path.join(downloads_path, "*"))

    # Ordenando os arquivos por tempo de modificação (mais recente primeiro)
    sorted_files = sorted(all_files, key=os.path.getmtime, reverse=True)

    #Caminho do arquivo mais recentemente modificado
    ultimo_arquivo_baixado = sorted_files[0]
    return ultimo_arquivo_baixado

pasta_downloads = r'C:/Users/40417601/Downloads'

def renomear_arquivo_e_mover(destino,pasta_downloads):
        ultimo_arquivo = encontrar_ultimo_arquivo(pasta_downloads)
        try:
            # Renomeia o arquivo
            os.rename(ultimo_arquivo, destino)
            return 1
        #Retorna erro se o arquivo não for encontrado
        except FileNotFoundError:
            return 0

def login(link_do_site):
    driver.get(link_do_site)
    time.sleep(3)
    driver.find_element(By.NAME, "tenant_id").clear() #Limpa o campo de preenchimento do email
    driver.find_element(By.NAME, "tenant_id").send_keys("Telefonica" )
    driver.find_element(By.CLASS_NAME,"button").click() #procura o elemento do menu
    time.sleep(1)


    driver.find_element(By.ID, "userIdentifier").clear() #Limpa o campo de preenchimento do email
    driver.find_element(By.ID, "userIdentifier").send_keys("*********" )
    driver.find_element(By.ID,"submitButton").click() #procura o elemento do menu
    time.sleep(1)

    driver.find_element(By.ID, "password").clear() #Limpa o campo de preenchimento do email
    driver.find_element(By.ID, "password").send_keys("*********")
    driver.find_element(By.ID,"submitButton").click() #procura o elemento do menu
    time.sleep(13)


arquivo_excel = 'C:/caminho/Base Censo Diversidade/Base.xlsx' #Caminho do arquivo contendo os dados dos colaboradores


censo = pd.read_excel(arquivo_excel)


driver = webdriver.Chrome() #Define o driver do navegador Chrome que vamos usar

driver.maximize_window() #



link = "https://sign.acesso.io/panel" #Link do site que vamos acessar para baixar os resultados do censo

nome = censo['Nome completo'] #Coluna do DataFrame contendo os nomes do colaboradores que serão pesquisados no site
chave = censo['Chave'] #Coluna do DataFrame contendo o nome que vamos salvar o arquivo que será baixado

pendencias = open("pendencias.txt","a") #Arquivo .txt contendo os colaboradores que não foram baixados resultados do censo


login(link) #Inicia o driver e faz login no site com as credenciais

for i in range(len(censo)): #Itera os colaboradores presentes na planilha
        
        time.sleep(3) #Função que faz o programa aguardar 3 segundos para evitar problemas com conexão a internet

        try: # O site devolve um erro de time out quando acessado muitas vezes seguidas e caso isso aconteça é necessário refazer o login
            error = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/octopus-envelope-management/div/oct-error-box/div/h2")
            time.sleep(2)
            if error and "Cliente não autorizado" in error.get_attribute("innerText"):
                login(link) # Refaz o login
            else:
                pass
        except NoSuchElementException: # Caso esse erro não seja encontrado, segue com o script
            pass         

        driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/octopus-envelope-management/div/div[1]/div[2]/oct-input/div/div/input").clear() #Limpa o campo de preenchimento do email
        pesquisa_nome = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/octopus-envelope-management/div/div[1]/div[2]/oct-input/div/div/input")
        pesquisa_nome.send_keys("%s"%(nome[i])) #Insere na caixa de pesquisa o nome do colaborador da vez
        
        time.sleep(3)
        pesquisa_nome.send_keys(Keys.ENTER) #Clica no botão de pesquisa

        time.sleep(4)
        try:
            envelope = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/octopus-envelope-management/div/div[4]/table/tbody/oct-block-envelope-table-row/tr/td[2]/span")
            if envelope and "Modelo_AutoDeclaração Racial_v3" in envelope.get_attribute("innerText"):
                # Confere se a declaração existe
                envelope.click()
                time.sleep(5)

                donwload_btn = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/octopus-envelope-management/oct-block-envelope-details/div/div[2]/div[1]/div[3]/oct-button[2]/button")
                donwload_btn.click() # Clica no botão para fazer download
                time.sleep(3)

                try: #Caso esse envelope não exista e um botão diferente esteja no lugar esperado
                    nao_btn = driver.find_element(By.XPATH,'/html/body/div[3]/div/div[2]/div/div/div/octopus-envelope-management/oct-block-envelope-details/div/oct-block-cancel-modal/oct-modal/div[2]/oct-button[1]/button')
                    time.sleep(1)
                    if  nao_btn and "Não" in  nao_btn.get_attribute("innerText"):
                        time.sleep(2)
                        nao_btn.click()
                        time.sleep(2)
                        #Clica na seta de "voltar" para pesquisarmos o próximo colaborador
                        driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/octopus-envelope-management/oct-block-envelope-details/div/div[1]/oct-button").click()
                        time.sleep(2) 
                        pendencias.write("%s\n"%(chave[i])) #Escreve no arquivo pendências.txt
                        continue
                    else:
                        pass
                except NoSuchElementException:
                     pass   

                time.sleep(3)
                #Salva o arquivo baixado e troca seu nome como a Chave do colaborador

                diretorio_destino = ('C:/caminho/Base Censo Diversidade/envelopes/%s.pdf'%(chave[i]))
                renomear_arquivo_e_mover(diretorio_destino,pasta_downloads)

                time.sleep(2)

                #Seta de voltar para continuarmos com o próximo colaborador
                driver.find_element(By.XPATH, "/html/body/div[3]/div/div[2]/div/div/div/octopus-envelope-management/oct-block-envelope-details/div/div[1]/oct-button").click()
                time.sleep(2)      
            else:
                print("Não existe envelope para %s ou algum erro foi encontrado"%(chave[i]))
                pendencias.write("%s\n"%(chave[i])) #Escreve no arquivo pendências.txt

        except NoSuchElementException:
            print("Não existe envelope para %s ou algum erro foi encontrado"%(chave[i]))
            pendencias.write("%s\n"%(chave[i])) #Escreve no arquivo pendências.txt
            continue
              

driver.quit() #Fecha o navegador
