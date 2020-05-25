from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests 

from . import models

BASE_CRAIGLIST_URL = "https://losangeles.craigslist.org/search/bbb?query={}"

# Create your views here.

def Search (request):
    return render (request , 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search = search)
    
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    
    response = requests.get(final_url)
    data = response.text

    soup = BeautifulSoup(data, 'html.parser')
    post_listings = soup.find_all('li' , {'class':'result-row'})
    
    final_posting = []
    
    x=0
    for post in post_listings:
        if x == 4:
            break
        
        post_title = post.find(class_ = 'result-title').text
        post_url = post.find('a').get('href')
        
        if post.find(class_="result-price"):
            post_price = post.find(class_="result-price").text
        else:
            post_price = "N/A" 


        pic_url = post_url
        details_url = requests.get(pic_url).text
        soup = BeautifulSoup(details_url , 'html.parser')

        if soup.find('img'):
            pic_of_post = soup.find("img").get('src')
        else:
            pic_of_post = None

        final_posting.append((post_title , post_url , post_price , pic_of_post))
        x+=1

    
    stuff_for_frontend = {
        "search":search,
        "final_postings":final_posting,
    }
    return render(request , 'new_search.html' , stuff_for_frontend)