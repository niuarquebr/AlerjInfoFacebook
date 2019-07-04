import DomExtract as service
import ConFacebook as face

serv = service.DomExtract()

"""Passo 1 - Carrega dados dos Deputados"""
retDeps = serv.cargaAlerjDeputados("http://www.alerj.rj.gov.br","/Deputados/QuemSao")
#print(retDeps[0])

"""Passo 2 - Realiza carga dos Projetos"""
#http://alerjln1.alerj.rj.gov.br/scpro1923.nsf/Internet/LeiInt?OpenForm&Count=5
retProj = serv.cargaAlerjProjetos("http://alerjln1.alerj.rj.gov.br","/scpro1923.nsf/Internet/LeiInt?OpenForm&Count=25")
#print(retProj)

"""Passo 3 - Formata dados em msg para postagem no facebook"""
retMSG = serv.formatarModeloMSG(retProj)
#print(retMSG[0],retMSG[1])

"""Passo 4 - Realiza postagem na pagina do facebook"""
gruposFace = ['2143033789279339']
face.enviarFacebookGroup(retMSG,gruposFace)


