
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
    
    tables = soup.find_all('tbody')
    tab = tables[1].find_all('tr')[:-1]

    data = {
        'state' : list(),
        'indian' : list(),
        'foreign' : list(),
        'discharged' : list(),
        'death' : list()
    }

    for row in tab[:-1]:
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
    tab = tables[1].find_all('tr')[:-1]

    data = {
        'state' : list(),
        'indian' : list(),
        'foreign' : list(),
        'discharged' : list(),
        'death' : list()
    }

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
    else:
        pass

    data=pd.DataFrame(list(zip(indian,foreign,discharged,death)),columns=['Indian','Foregin','Discharged','Death'],index=state)
    data['total']=data['Indian']+data['Foregin']+data['Discharged']+data['Death']
    data.sort_values(by='total',axis=0,ascending=False,inplace=True)
    statewise = data.to_dict()
    """
    counts=soup.findAll("span", {"class": "icount"})
    label=soup.findAll("div", {"class": "info_label"})
    info=dict()
    for i in range(len(counts)):
        info[remove_html_tags(label[i])]=[0]
    for i in range(len(counts)):
        info[remove_html_tags(label[i])].append(get_count(remove_html_tags(counts[i])))
    """

    print(json.dumps(data))
    return render(req,'home.html',{'data': mark_safe(json.dumps(data))})
    #return JsonResponse(data)
    #return HttpResponse(response.text)