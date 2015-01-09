import requests
from bs4 import BeautifulSoup
import os

#Lista de peliculas
movieName = "Terminator"
movieYear = "1984"
    
#Busqueda en FA
session = requests.Session()
results = 0
r = session.get("http://www.filmaffinity.com/es/search.php?stype=title&stext="+movieName+"&from="+str(results))    
r.enconding = 'UTF-8'
data = r.text
soup = BeautifulSoup(data)
if soup.find('div',{"sub-header-search":True}) is None:
    #Varios resultados
    titleYear = soup.find('div',{"class":"mc-title"})
    print titleYear.text
    results += 50   
    r = session.get("http://www.filmaffinity.com/es/search.php?stype=title&stext="+movieName+"&from="+str(results))    
    r.enconding = 'UTF-8'
    data = r.text
    soup = BeautifulSoup(data)

