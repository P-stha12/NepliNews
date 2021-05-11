from django.shortcuts import render
import requests
import random
from bs4 import BeautifulSoup

# Create your views here.


def ratopati():
    news = []
    req = requests.get('http://ratopati.com/category/coronavirus')
    soup = BeautifulSoup(req.text, 'lxml')
    articles = soup.find_all('div', {'class':'item'})[0:10]
    for article in articles:
        d = {}
        d['source'] = 'Ratopati'
        d['img_link'] = article.find('a', {'class':'item-header-image'}).find('img').attrs['src']
        d['content'] = article.find('p').text
        div = article.find('div', {'class':'item-content'})
        d['title'] = div.find('a').text
        d['news_link'] = div.find('a').attrs['href']
        d['news_link'] = 'https://ratopati.com' + d['news_link']
        news.append(d)
    return news


def news24():
    news = []
    req = requests.get('https://bit.ly/3vJArGQ')
    soup = BeautifulSoup(req.text, 'lxml')
    articles = soup.find_all('div', {'class':'col-md-12'})[1:10]
    for article in articles:
        d = {}
        d['source'] = 'News24'
        links = article.find_all('a')
        d['img_link'] = links[0].find('img').attrs['src']
        d['news_link'] = links[1].attrs['href']
        d['title'] = article.find('h2').text
        d['content'] = article.find('p').text
        news.append(d)
    return news


def home(request):
    news = ratopati() + news24()
    random.shuffle(news)
    return render(request, 'aggregator/index.html', {'articles': news})
