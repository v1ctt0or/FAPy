# -*- coding: utf-8 -*-
import GenreClassification
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

def faSamePage(url1, url2):
    soup1 = GenreClassification.getSoup(url1)
    soup2 = GenreClassification.getSoup(url2)
    return soup1.find('div',{"class":"pager"}) == soup2.find('div',{"class":"pager"})
    
def faGetUserMovieList(userId):
    faMovieIds = []
    pag = 0
    while True:
        movieIds = []
        pag += 1
        soup = GenreClassification.getSoup("http://www.filmaffinity.com/es/userratings.php?user_id="+userId+"&p="+str(pag)+"&orderby=4")
        movieIds = soup.findAll('div',{"data-movie-id":True})
        for movieId in movieIds:
            faMovieIds.append(str(movieId['data-movie-id']))
        if faSamePage("http://www.filmaffinity.com/es/userratings.php?user_id="+userId+"&p="+str(pag)+"&orderby=4","http://www.filmaffinity.com/es/userratings.php?user_id="+userId+"&p="+str(pag+1)+"&orderby=4"):
            break
        time.sleep(3)
    return faMovieIds

def faGetName(movieId, original):
    soup = GenreClassification.getSoup("http://www.filmaffinity.com/es/film"+movieId+".html")
    if original:
        title = soup.findAll('dd')[0].text
    else:
        title = soup.find('h1',{"id":"main-title"}).text
    return title
    
def main(userId, path):
    pcMovieIds = []
    faMovieIds = []
    
    #Lista de Ids de guardadas
    for fileName in os.listdir(path):
        #Extraccion de nombre y año de la pelicula
        movieName, movieYear = GenreClassification.fileParser(fileName)

        if not(movieName is '' or movieYear is ''):
            #Busqueda en FA
            time.sleep(0.5)
            movieId = GenreClassification.filmFinder(movieName, movieYear)
            pcMovieIds.append(movieId)
    
    #Lista de Ids de votadas
    faMovieIds = faGetUserMovieList(userId)
    print("Peliculas que tengo ("+str(len(pcMovieIds))+"): ", pcMovieIds)
    print("------------------------------------------------------------------")
    print("Peliculas votadas ("+str(len(faMovieIds))+"): ", faMovieIds)
    print("******************************************************************")
    print("Peliculas votadas y que tengo: ", set(faMovieIds) & set(pcMovieIds))
    print("------------------------------------------------------------------")
    print("Peliculas votadas y que no tengo:", set(faMovieIds) - set(pcMovieIds))
    print("------------------------------------------------------------------")
    print("Peliculas no votadas y que tengo:", set(pcMovieIds) - set(faMovieIds))

if __name__ == '__main__':
    #main('236953', 'C:\\Data\\Personal\\Python\\GenreTest\\Film-tests')
    print(u"Original: " +faGetName('341251', True))
    print(u"Español: " +faGetName('341251', False))
