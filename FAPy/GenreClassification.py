# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import os
import time

def getSoup(url):
    session = requests.Session()
    r = session.get(url)
    r.encoding = 'UTF-8'
    data = r.text
    soup = BeautifulSoup(data)
    return soup

def fileParser(fileName):
    try:
        movie = []
        isFile = fileName.index('.') #Si tiene extension, es fichero
        if isFile > 0:
            if '(' in fileName:
                if fileName.index(' (') < fileName.index(' - '):
                    movieName = fileName.split(' (',1)[0].strip()
                else:
                    movieName = fileName.split(' - ',1)[0].strip()
            else:
                movieName = fileName.split(' - ',1)[0].strip()
            movieYear = fileName.split(' - ',1)[1].strip()[:4]
            return movieName, movieYear
    except (RuntimeError, TypeError, NameError, ValueError, IndexError):
        return '', ''

def filmFinder(movieName, movieYear):
    soup = getSoup("http://www.filmaffinity.com/es/advsearch.php?stext="+movieName+"&stype[]=title&country=&genre=&fromyear="+movieYear+"&toyear="+movieYear)
    movieId = soup.find('div',{"data-movie-id":True})
    return str(movieId['data-movie-id'])

def tagFinder(movieId, category):
    try:
        time.sleep(0.5)
        soup = getSoup("http://www.filmaffinity.com/es/film"+movieId+".html")
        if category == 'GENRE':
            tags = soup.find('meta',{"property":"og:description"})['content']
            tag = tags[tags.index(u'Género: ')+8:].split('|',1)[0]
        else:
            i = 0
            tag = ''
            for dt in soup.findAll('dt'):
                if category == 'COUNTRY':
                    if dt.text == u'País':
                        tag = soup.findAll('dd')[i].text.strip()
                elif category == 'YEAR':
                   if dt.text == u'Año':
                       tag = soup.findAll('dd')[i].text.strip()
                elif category == 'DIRECTOR':
                   if dt.text == u'Director':
                       tag = soup.findAll('dd')[i].text.strip()
                elif category == 'DURATION':
                   if dt.text == u'Duración':
                       tag = soup.findAll('dd')[i].text.strip()
                elif category == 'CAST':
                   if dt.text == u'Reparto':
                       tag = soup.findAll('dd')[i].text.strip()
                i += 1
        return tag
    except (RuntimeError, TypeError, NameError, ValueError, IndexError):
        return ''

def createDir(path, name):
    try:
        moviePath = path+'\\'+name.strip()
        if not os.path.exists(moviePath):
            os.makedirs(moviePath)
        return moviePath
    except (RuntimeError, AttributeError, TypeError, NameError, ValueError, IndexError):
        pass

def moveFile(iniPath, finPath, fileName):
    os.rename(iniPath+'\\'+fileName, finPath+'\\'+fileName)

def main(path, classification):
    for fileName in os.listdir(path):
        #Extraccion de nombre y año de la pelicula
        movieName, movieYear = fileParser(fileName)
        print(movieName, movieYear)
        if not(movieName is '' or movieYear is ''):    
            #Busqueda en FA
            time.sleep(0.5)
            movieId = filmFinder(movieName, movieYear)
            print(movieId)

            #Busqueda de genero
            time.sleep(0.5)
            if classification.upper() == 'GENRE':
                movieCategory = tagFinder(movieId, 'GENRE')
            elif classification.upper() == 'COUNTRY':
                movieCategory = tagFinder(movieId, 'COUNTRY')
            elif classification.upper() == 'YEAR':
                movieCategory = tagFinder(movieId, 'YEAR')
            elif classification.upper() == 'DIRECTOR':
                movieCategory = tagFinder(movieId, 'DIRECTOR')
            elif classification.upper() == 'DURATION':
                movieCategory = tagFinder(movieId, 'DURATION')
            elif classification.upper() == 'CAST':
                movieCategory = tagFinder(movieId, 'CAST')
            print(movieCategory)
            
            #Reubicacion de pelicula
            moviePath = createDir(path, movieCategory)
            moveFile(path, moviePath, fileName)
        
if __name__ == '__main__':
    #main('C:\\Data\\Personal\\Python\\GenreTest\\Film-tests','genre')
    print(tagFinder('341251', 'YEAR'))
    print(tagFinder('341251', 'COUNTRY'))
    print(tagFinder('341251', 'DURATION'))
    print(tagFinder('341251', 'DIRECTOR'))
    print(tagFinder('341251', 'GENRE'))
    print(tagFinder('341251', 'CAST').split(', ')[0])
