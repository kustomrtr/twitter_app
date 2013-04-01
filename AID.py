# coding: utf-8

# ===================================================================

# Usage: tw.py [action] [username] [page_count] 

# Options:
#     -action        Use 'img' to download images from the user and   
#                    use 'status' to retrieve latest user status
#     -username      Username to which you want to take the action.
#     -page_count    How much pages would you like to retrieve?

# ===================================================================


import twitter
import urllib2
import re
import os
import sys

def dlfile(url, usuario):
    try:
        f = urllib2.urlopen(url)
        print "Descargando: " + url
        filename = usuario[1:] + '_' + os.path.basename(url)[::2] +'.jpg'
        directorio = os.path.join(usuario[1:])

        if not os.path.isdir(directorio):
            os.makedirs(directorio)

        filename = os.path.join(directorio, filename)
        with open(filename, "wb") as local_file:
            local_file.write(f.read())


    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
        pass
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url
        pass

def bajarImagenes(usuario,page):
    api = twitter.Api()
    try:
        statuses = api.GetUserTimeline(usuario,count=800,include_rts=False, exclude_replies=True, page=page)
        print 'Bajando imagenes de', usuario, '( pagina: ', page, ')'
        for status in statuses:
            if 'http' in status.text: #si el tweet contiene una url
                match = re.match(r".*(http://t.co/\w+){1}$.*", status.text)
                if match: #si hay match, devuelve true      
                    uri = match.group(1)
                    try:
                        img_html = urllib2.urlopen(uri)
                        img_html = img_html.read()
                        matchImg = re.search(r'''.*((http|https)://pbs.twimg.com/media/.*\.jpg).*''', img_html)

                        if matchImg:
                            dlfile(matchImg.group(1), usuario)
                    except urllib2.HTTPError, e:
                        if matchImg:
                            print "HTTP Error:", e.code, matchImg.group(1)
                        pass
                    except urllib2.URLError, e:
                        if matchImg:
                            print "URL Error:", e.reason, matchImg.group(1)
                        pass
    except twitter.TwitterError:
        print 'ERROR: El usuario', usuario,'tiene la cuenta bloqueada. Intenta con otro usuario :('
        pass

def mostrarStatus(usuario,page):
    api = twitter.Api()
    try:
        statuses = api.GetUserTimeline(usuario,count=800,include_rts=False, exclude_replies=True, page=page)
        for status in statuses:
            print status.text.encode('utf-8')
    except twitter.TwitterError:
        print 'ERROR: El usuario', usuario,'tiene la cuenta bloqueada. Intenta con otro usuario :('
        pass

def inicio():
    pages = 0
    try:
        if sys.argv[1] == 'status':            
            try:
                pages = int(sys.argv[3])
            except ValueError:
                print 'Debes ingresar un numero entero para la paginacion'

            for page in range(pages):
                mostrarStatus('@'+sys.argv[2], page+1)
                
        elif sys.argv[1] == 'img':
            try:
                pages = int(sys.argv[3])
            except ValueError:
                print 'Debes ingresar un numero entero para la paginacion'

            for page in range(pages):
                bajarImagenes('@'+sys.argv[2], page+1)
        else:
            print 'Error en los argumentos.'
            print '''
===================================================================

Usage: tw.py [action] [username] [page_count] 

Options:
    -action        Use 'img' to download images from the user and   
                   use 'status' to retrieve latest user status
    -username      Username to which you want to take the action.
    -page_count    How much pages would you like to retrieve?

===================================================================
            '''
    except IndexError:
        print 'Ingresa todos los argumentos'

inicio()