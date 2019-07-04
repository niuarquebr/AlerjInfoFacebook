"""
https://www.json.org/json-pt.html
https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
https://gist.github.com/stupidbodo/614b6e77d54fb5870f3a

"""
import json
import os
from time import gmtime, strftime

def inicializarPastas():
    try:
        os.mkdir('json')
        os.mkdir('./json/deps')
        os.mkdir('./json/projs')
        print('inicializarPastas - Pastas Basicas criadas com sucesso.')
        return 1
    except OSError:
        print('inicializarPastas - Pastas Basicas ja criadas.')
        return 0

def carregarArquivo(pastaArq,nomeArq,prazo):
    try:
        data = []
        if(prazo!=None):
            prazo = '_' + strftime("%Y%m", gmtime())
            caminho = os.path.join(pastaArq, nomeArq) + prazo + '.json' 
        else:
            caminho = os.path.join(pastaArq, nomeArq) + '.json' 
        if(os.path.exists(caminho)):
            with open(caminho) as json_file:
                ret = json_file.read()
                #print(ret)
                data = json.loads(ret)
                #print(data)
                
        else:
            raise ValueError("Arquivo não encontrado.")
            
        print('cargarArquivo - Carga realizada no arquivo:',nomeArq)
        return 1, data
    except ValueError as exp:
        print('Erro cargarArquivo:',nomeArq,exp)
        return 0, data

def criarArquivo(pastaArq,nomeArq,prazo,conteudo):
    try:
        if(prazo!=None):
            prazo = '_' + strftime("%Y%m", gmtime())
            caminho = os.path.join(pastaArq, nomeArq) + prazo + '.json'
        else:
            caminho = os.path.join(pastaArq, nomeArq) + '.json'
        arq = open(caminho, 'w+')
        arq.writelines(str(json.dumps(conteudo)))
        arq.close()

        print('criarArquivo - Arquivo criado:',nomeArq)
    except ValueError as exp:
        print('Erro criarArquivo:',nomeArq)
        

        

 