"""
pip install requests
pip install beautifulsoup4
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

Dicionarios Python - Classes/Objects
https://docs.python.org/3/library/stdtypes.html#dict

"""

import requests 
import re
from bs4 import BeautifulSoup
import ConJSON as conJSON

class DomExtract():
   
    def __init__(self):
        r = requests.packages.urllib3.disable_warnings()  # desabilita os warnings
        self.deputadosArr =[]
        self.projetosArr =[]
        conJSON.inicializarPastas()

    def __cargaURL(self,url,headers,cookies):
        try:
            session = requests.Session()
            response = ""
            response = session.get(url, cookies=cookies, auth="",  headers=headers, verify=False, allow_redirects=True)
            return  response
        except (ValueError, KeyError, TypeError):
            print(ValueError)
            return "Erro: __cargaURL"
    
    def cargaAlerjProjetos(self,url1,url2):
        try:
            headers = {
                'Host': 'alerjln1.alerj.rj.gov.br',
                #'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'               
            } 
      
            response = self.__cargaURL(url1 + url2,headers,"")
            ret1 = BeautifulSoup(response.text, 'html.parser')
            #print(ret1.prettify())
            saida1 = ret1.find_all('table')[1]('tr')
            listaProjs =[]
            projetosArr = []
            ret,projetosArr = conJSON.carregarArquivo('json/projs','listaProjs',None)

            for key,item in enumerate(saida1):
                if((key>=1) and (item('td')[0].text not in projetosArr)):
                    desc_det = item('td')[2].text.split("=>")
                    deps_proj = item('td')[4].text.split(",")
                    ret_contatos = self.retornarContatos(deps_proj[0])
                    objDICT = {"link_proj": url1 + item('td')[0]('a')[0].get('href')
                            , "codi_proj": item('td')[0].text
                            , "nume_proj": '{}/{}'.format(item('td')[0].text[-5:],item('td')[0].text[:4])
                            , "desc_proj": desc_det[0].lstrip("\n")
                            , "tags_proj": desc_det[2].lstrip("\n")
                            , "data_proj": item('td')[3].text     
                            , "deps_proj": item('td')[4].text    
                            
                            , "part_dep": ret_contatos[0]
                            , "tele_dep": ret_contatos[1]
                            , "email_dep": ret_contatos[2]                            
                            }
                    listaProjs.append(objDICT)
                    projetosArr.append(item('td')[0].text)
                    
            conJSON.criarArquivo('json/projs','listaProjs',None,projetosArr)
                        
            self.projetosArr = projetosArr
            return listaProjs
        except (ValueError, KeyError, TypeError):
            print('cargaAlerjProjetos',ValueError)
            return []           
        
    def cargaAlerjDeputados(self,url1,url2):
        try:
            headers = {
                'Host': 'www.alerj.rj.gov.br',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
            }

            ret,listaDeps = conJSON.carregarArquivo('json/deps','listaDeps',True)
            if(ret==0):
                response = self.__cargaURL(url1 + url2,headers,"")
                ret1 = BeautifulSoup(response.text, 'html.parser')
                saida1 = ret1.findAll("div", {"class": "controle_deputado"})
                listaDeps = []
                
                for key,item in enumerate(saida1):
                    saidaDetDep = self.cargaAlerjDetalhesDeputados(url1,item('a')[0].get('href'))
                    objDICT = {"key": key
                            , "link_dep": url1 + item('a')[0].get('href')
                            , "nome_dep": item('a')[0]('img')[0].get('alt')
                            , "link_foto": url1 + item('a')[0]('img')[0].get('src')
                            , "part_dep": item('div')[2].text
                            , "nome_full": saidaDetDep[0]     
                            , "tele_dep": saidaDetDep[1]
                            , "email_dep": saidaDetDep[2]
                            }
                    listaDeps.append(objDICT)
                conJSON.criarArquivo('json/deps','listaDeps',True,listaDeps)
                
            self.deputadosArr = listaDeps
            return listaDeps
    
        except (ValueError, KeyError, TypeError):
            print(ValueError)
            return "Erro: cargaAlerjDeputados"
            
    def cargaAlerjDetalhesDeputados(self,url1,url2):
        try:
            headers = {
                'Host': 'www.alerj.rj.gov.br',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
            }
            
            response = self.__cargaURL(url1 + url2,headers,"")
            ret1 = BeautifulSoup(response.text, 'html.parser')
            saida1 = ret1.findAll("div", {"class": "descricao"})
            #print(saida1[1].prettify())
            """
            print('Nome Full:',saida1[1]('h1')[0].text)
            print('Telefone:',saida1[1]('p')[len(saida1[1]('p'))-2].text)
            print('E-mail:',saida1[1]('p')[len(saida1[1]('p'))-1].text)
            """
            result = [saida1[1]('h1')[0].text
                    ,saida1[1]('p')[len(saida1[1]('p'))-2].text
                    ,saida1[1]('p')[len(saida1[1]('p'))-1].text
                    ]
            return result
            
        except (ValueError, KeyError, TypeError):
            print(ValueError)
            return "Erro: cargaAlerjDetalhesDeputados"
             
    def formatarModeloMSG(self,listaDados):
        try:
            resultArr = []           
            for item in listaDados:
                result = """ALERJ - Assembleia Legislativa do Estado do Rio de Janeiro \n
Projeto de Lei(Nº): {}
Data de publicação: {}
Deputado(a) autor(a): {} - {} \n
Texto Projeto: {} 
Link Projeto: {} \n
Segue contatos:
Telefone: {}
E-mail: {} 

Como avalia essa Projeto?
👍(Aprova) 😡(Reprova)
"""
                
                resultArr.append(result.format(item['nume_proj']
                                                ,item['data_proj']
                                                ,item['deps_proj']
                                                ,item['part_dep']
                                                ,item['desc_proj']
                                                ,item['link_proj']
                                                ,item['tele_dep']
                                                ,item['email_dep']))
            return resultArr
        
        except (ValueError, KeyError, TypeError):
            print(ValueError)
            return "Erro: formatarModeloMSG"
            
    def retornarContatos(self,procurado):
        try:
            resultArr = ['','','']
            for item in self.deputadosArr:
                if(item['nome_dep']==procurado):
                    resultArr = [item['part_dep'],item['tele_dep'],item['email_dep']]
                    
            return resultArr
        except (ValueError, KeyError, TypeError):
            print("Erro: retornarContatos",ValueError)
            return "Erro: retornarContatos"
    