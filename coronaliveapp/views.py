
import requests, json
import pandas as pd
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
    
    tables = soup.find_all('tbody')
    tab=soup.find_all('tr')

    state=list()
    indian=list()
    foreign=list()
    discharged=list()
    death=list()

    for row in tab:
        lst=row.find_all('td')
        if(len(lst)==6):
            try:
                state.append((remove_html_tags(lst[1])))
                indian.append(get_count(remove_html_tags(lst[2])))
                foreign.append(get_count(remove_html_tags(lst[3])))
                discharged.append(get_count(remove_html_tags(lst[4])))
                death.append(get_count(remove_html_tags(lst[5])))
            except:
                pass

    data=pd.DataFrame(list(zip(state,indian,foreign,discharged,death)),columns=['state','indian','foreign','discharged','death'])
    data['total']=data['indian']+data['foreign']+data['discharged']+data['death']
    data.sort_values(by='total',axis=0,ascending=False,inplace=True)
    statewise = data.to_dict()
    info=dict()
    for ke in statewise:
        statewise[ke]=list(statewise[ke].values())
    counts=soup.findAll("span", {"class": "icount"})
    label=soup.findAll("div", {"class": "info_label"})
    info_labels=['passengers','total','cured','death','migrated']
    info_counts=[remove_html_tags(x) for x in counts]
    info=dict(zip(info_labels,info_counts))
    print(json.dumps(statewise))
    return render(req,'home.html',{'data': mark_safe(json.dumps(statewise)),'info':mark_safe(json.dumps(info)),'info2':json.dumps(info)})
    #return JsonResponse(data)
    #return HttpResponse(response.text)


def remove_html_tags(text):
    """Remove html tags from a string"""
    text=str(text)
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def get_count(text):
    text=str(text)
    num=int(re.findall(r'\d+', text)[0])
    return num

def ping(req):
    return HttpResponse('<h1>pong</h1>')

def adarsh_home(req):
    url = "https://www.mohfw.gov.in/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    tables = soup.find_all('tbody')
    tab=soup.find_all('tr')

    state=list()
    indian=list()
    foreign=list()
    discharged=list()
    death=list()

    for row in tab:
        lst=row.find_all('td')
        if(len(lst)==6):
            try:
                state.append((remove_html_tags(lst[1])))
                indian.append(get_count(remove_html_tags(lst[2])))
                foreign.append(get_count(remove_html_tags(lst[3])))
                discharged.append(get_count(remove_html_tags(lst[4])))
                death.append(get_count(remove_html_tags(lst[5])))
            except:
                pass

    data=pd.DataFrame(list(zip(state,indian,foreign,discharged,death)),columns=['state','indian','foreign','discharged','death'])
    data['total']=data['indian']+data['foreign']+data['discharged']+data['death']
    data.sort_values(by='total',axis=0,ascending=False,inplace=True)
    statewise = data.to_dict()
    for ke in statewise:
        statewise[ke]=list(statewise[ke].values())
    counts=soup.findAll("span", {"class": "icount"})
    label=soup.findAll("div", {"class": "info_label"})
    info_labels=['passengers','total','cured','death','migrated']
    info_counts=[remove_html_tags(x) for x in counts]
    info=dict(zip(info_labels,info_counts))
    return render(req,'home.html',{'data': mark_safe(json.dumps(statewise)),'info':mark_safe(json.dumps(info),),'info2':json.dumps(info)})
    #return JsonResponse(data)
    #return HttpResponse(response.text)