import os #Biblioteca para mover e manipular arquivos do computador

from pdf2jpg import pdf2jpg #Biblioteca que converte PDF para JPG

def renomear_arquivo_e_mover(origem, destino):
        try:
            # Renomeia o arquivo
            os.rename(origem, destino)
            return 1
        
        except FileNotFoundError:
            return print('Erro!')
        
# Diretório alvo 
diretorio = 'C:/caminho/Base Censo Diversidade/envelopes'

# Obtém a lista de arquivos no diretório
lista_de_arquivos = os.listdir(diretorio)

# Filtra apenas os arquivos (ignora diretórios)
arquivos = [arquivo for arquivo in lista_de_arquivos if os.path.isfile(os.path.join(diretorio, arquivo))]

# Exibe a lista de nomes de arquivos
for i in range(len(arquivos)) :
    diretorio_pdf = 'C:/caminho/Base Censo Diversidade/envelopes/' + '%s'%(arquivos[i])
    outputpath = r"C:/caminho/Base Censo Diversidade/prints/"
    result = pdf2jpg.convert_pdf2jpg(diretorio_pdf,outputpath, pages="0") # Função que converte os tipos

    # Após o print mover para a pasta única para facilitar a visualização
    
    diretorio_inicial = 'C:/caminho/Base Censo Diversidade/prints/%s_dir/0_%s.jpg'%(arquivos[i],arquivos[i])
    diretorio_geral =  'C:/caminho/Base Censo Diversidade/prints/printsGerais/%s.jpg'%(arquivos[i])
    renomear_arquivo_e_mover(diretorio_inicial,diretorio_geral)

    # Apagar diretorio inicial
    diretorio_inicial = 'C:/Users/40417601/Desktop/Base Censo Diversidade/prints/%s_dir'%(arquivos[i])
    os.rmdir(diretorio_inicial)

