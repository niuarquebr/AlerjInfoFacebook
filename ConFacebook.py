"""
Publicando no Facebook
http://nodotcom.org/python-facebook-tutorial.html
https://blog.theodo.com/2019/02/automatically-publish-facebook-pages-python/
https://www.piliapp.com/facebook-symbols/

https://www.pythoncircle.com/post/666/automating-facebook-page-posts-using-python-script/
"""
import re
import requests

def enviarFacebookGroup(listaMSG,listaGrupos):
    try:

        session = requests.session()
        username = "niuarquebr@yahoo.com.br"
        password = ""
        #uid, dtsg = login(session, username, password)
    
        for key,grupo in enumerate(listaGrupos):
            for key,msg in enumerate(listaMSG):
                #postFacebookGroup(session, dtsg, grupo, msg ,uid)
                print(grupo, msg)
                
    except (ValueError, KeyError, TypeError):
        print(ValueError)

def login(session, username, password):
    # Navigate to the Facebook homepage
    response = session.get('https://facebook.com')
    
    # load lsd, one const var acess
    lsd = re.search(r'name="lsd" value="([0-9a-zA-Z-_:]+)"', response.text).group(1)
    data={'lsd': lsd,'email': username,'pass': password,'default_persistent': '0','timezone': '-60','locale':'pt_BR'}
    
    try:
        # Perform the login request
        response = session.post('https://www.facebook.com/login.php?login_attempt=1',data )

        uid = session.cookies['c_user']        
        dtsg = re.search(r'(type="hidden" name="fb_dtsg" value="([0-9a-zA-Z-_:]+)")', response.text).group(1)

        dtsg = dtsg[dtsg.find("value")+6:]
        dtsg = dtsg[1:-1]

    except KeyError:
        raise Exception('Login Failed!')

    return uid, dtsg


def postFacebookGroup(session, dtsg, pageID, message,uID):
    try:
        data = {"fb_dtsg":dtsg,"message":message,"target":pageID}
        response = session.post('https://m.facebook.com/a/group/post/add/?gid='+pageID+'&refid=18',data=data,headers = {'Content-Type':'application/x-www-form-urlencoded'})
    
        print(response)

    except Exception:
        print("Erro")
        
def postFacebookTL(session, dtsg, pageID, message,uID):
    try:
        data = {"fb_dtsg":dtsg,"message":message,"target":pageID}
        response = session.post('https://m.facebook.com/a/group/post/add/?gid='+pageID+'&refid=18',data=data,headers = {'Content-Type':'application/x-www-form-urlencoded'})
    
        print(response)

    except Exception:
        print("Erro")        