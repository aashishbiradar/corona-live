
import requests, json
import urllib.request
import time
from bs4 import BeautifulSoup
import re
from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe
from django.shortcuts import render

def home(req):
    url = "https://www.mohfw.gov.in/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tab = soup.find_all('tr')

    data = {
        'state' : list(),
        'indian' : list(),
        'foreign' : list(),
        'discharged' : list(),
        'death' : list()
    }

    for row in tab[1:-1]:
        lst = row.find_all('td')
        data['state'].append(remove_html_tags(lst[1]))
        data['indian'].append(int(remove_html_tags(lst[2])))
        data['foreign'].append(int(remove_html_tags(lst[3])))
        data['discharged'].append(int(remove_html_tags(lst[4])))
        data['death'].append(int(remove_html_tags(lst[5])))
    print(json.dumps(data))
    return render(req,'home.html',{'data': mark_safe(json.dumps(data))})
    #return JsonResponse(data)
    #return HttpResponse(response.text)


def remove_html_tags(text):
    """Remove html tags from a string"""
    text=str(text)
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def ping(req):
    return HttpResponse('<h1>pong</h1>')