
import requests, json, re, urllib.request, time, tweepy

import pandas as pd
from datetime import datetime, date
from bs4 import BeautifulSoup, Comment

from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.utils import timezone
from coronaliveapp.config import CONFIG
from corona.models import Cache, Daily

#route functions
def home(req):
    t1 = time.time()
    cache_key = 'homepage'
    expiry = 5 
    cached_data = get_cache(cache_key, expiry)
    from_cache= 'true'

    if not cached_data:
        try:
            soup=get_mohfw()
            statewise=get_statewise(soup)
            wiki=get_wiki()
            tests=get_tests(wiki)

            #latest data
            latest = get_info(soup)
            updated = False

            try:
                latest_rec = Daily.objects.get(date = date.today())
                if int(latest['confirmed']) > latest_rec.confirmed:
                    updated = True
                latest_rec.confirmed = int(latest['confirmed'])
                latest_rec.active = int(latest['infected'])
                latest_rec.recovered = int(latest['cured'])
                latest_rec.death = int(latest['death'])
                latest_rec.source = latest['source']
            except Daily.DoesNotExist:
                latest_rec = Daily(
                    date = date.today(),
                    confirmed = int(latest['confirmed']),
                    active = int(latest['infected']),
                    recovered = int(latest['cured']),
                    death = int(latest['death']),
                    source = latest['source']
                )
            latest_rec.save()

            #try:
            #    if updated:
            #        tweet_update(latest)
            #except:
            #    pass

            #daily data
            daily_df = pd.DataFrame(Daily.objects.all().values())
            daily_df['date'] = pd.to_datetime(daily_df['date'])
            daily_df.sort_values(by=['date'], inplace=True)
            daily_df['date'] = daily_df['date'].dt.strftime('%b %d')
            
            days = {
                'date': daily_df['date'].tolist(),
                'confirmed': daily_df['confirmed'].tolist(),
                'recovered': daily_df['recovered'].tolist(),
                'death': daily_df['death'].tolist()
            }
            days['confirmedincrease']=[days['confirmed'][0]]
            days['recoveredincrease']=[days['recovered'][0]]
            days['deathincrease']=[days['death'][0]]
            for i in range(1,len(days['confirmed'])):
                days['confirmedincrease'].append(days['confirmed'][i]-days['confirmed'][i-1])
                days['recoveredincrease'].append(days['recovered'][i]-days['recovered'][i-1])
                days['deathincrease'].append(days['death'][i]-days['death'][i-1])

            """
            days['predict']=list()
            for i in range(0,4):
                days['predict'].append(days['confirmed'][i])
            for i in range(4,len(days['confirmed'])):
                days['predict'].append(int(days['predict'][i-1]*0.17+days['predict'][i-1]))
            """
            info = {
                'confirmed': days['confirmed'][-1],
                'active': daily_df['active'].tolist()[-1],
                'recovered': days['recovered'][-1],
                'death': days['death'][-1],
                'diffconfirmed': days['confirmed'][-1]-days['confirmed'][-2],
                'diffactive': daily_df['active'].tolist()[-1]-daily_df['active'].tolist()[-2],
                'diffrecovered': days['recovered'][-1]-days['recovered'][-2],
                'diffdeath': days['death'][-1]-days['death'][-2]
            }

            info['percentageconfirmed']=round(info['diffconfirmed']*100/days['confirmed'][-2])
            info['percentageactive']=round(info['diffactive']*100/daily_df['active'].tolist()[-2])
            info['percentagerecovered']=round(info['diffrecovered']*100/days['recovered'][-2])
            info['percentagedeath']=round(info['diffdeath']*100/days['death'][-2])

            cached_data = {
                'statewise': statewise,
                'info': info,
                'days': days,
                'tests': tests,
            }

            save_cache(cache_key, cached_data)
            from_cache= 'false'
        except:
            cached_data = get_cache(cache_key)

        
    t2 = time.time()
    compute = t2-t1
    return render(req,'home.html',{
        'data': mark_safe(json.dumps(cached_data)),
        'compute': compute,
        'from_cache': from_cache,
        'dict': cached_data
    })


#route functions
def adarsh(req):
    t1 = time.time()
    cache_key = 'adarsh'
    expiry = 5 
    cached_data = get_cache(cache_key, expiry)
    from_cache= 'true'

    if True or not cached_data:
        soup=get_mohfw()
        statewise=get_statewise(soup)
        wiki=get_wiki()
        tests=get_tests(wiki)
        
        #latest data
        latest = get_info(soup)
        updated = False
        try:
            latest_rec = Daily.objects.get(date = date.today())
            if int(latest['confirmed']) > latest_rec.confirmed:
                updated = True
            latest_rec.confirmed = int(latest['confirmed'])
            latest_rec.active = int(latest['infected'])
            latest_rec.recovered = int(latest['cured'])
            latest_rec.death = int(latest['death'])
            latest_rec.source = latest['source']
        except Daily.DoesNotExist:
            latest_rec = Daily(
                date = date.today(),
                confirmed = int(latest['confirmed']),
                active = int(latest['infected']),
                recovered = int(latest['cured']),
                death = int(latest['death']),
                source = latest['source']
            )
        latest_rec.save()


        try:
            if updated:
                tweet_update(latest)
        except:
            pass


        #daily data
        daily_df = pd.DataFrame(Daily.objects.all().values())
        daily_df['date'] = pd.to_datetime(daily_df['date'])
        daily_df.sort_values(by=['date'],inplace=True)
        daily_df['date'] = daily_df['date'].dt.strftime('%b %d')
        
        days = {
            'date': daily_df['date'].tolist(),
            'confirmed': daily_df['confirmed'].tolist(),
            'recovered': daily_df['recovered'].tolist(),
            'death': daily_df['death'].tolist()
        }
        days['confirmedincrease']=[days['confirmed'][0]]
        days['recoveredincrease']=[days['recovered'][0]]
        days['deathincrease']=[days['death'][0]]
        for i in range(1,len(days['confirmed'])):
            days['confirmedincrease'].append(days['confirmed'][i]-days['confirmed'][i-1])
            days['recoveredincrease'].append(days['recovered'][i]-days['recovered'][i-1])
            days['deathincrease'].append(days['death'][i]-days['death'][i-1])


        days['predict']=list()
        for i in range(0,4):
            days['predict'].append(days['confirmed'][i])
        for i in range(4,len(days['confirmed'])-1):
            days['predict'].append(days['confirmed'][i]*0.15+days['confirmed'][i])

        info = {
            'confirmed': days['confirmed'][-1],
            'active': daily_df['active'].tolist()[-1],
            'recovered': days['recovered'][-1],
            'death': days['death'][-1],
            'diffconfirmed': days['confirmed'][-1]-days['confirmed'][-2],
            'diffactive': daily_df['active'].tolist()[-1]-daily_df['active'].tolist()[-2],
            'diffrecovered': days['recovered'][-1]-days['recovered'][-2],
            'diffdeath': days['death'][-1]-days['death'][-2]
        }

        info['percentageconfirmed']=round(info['diffconfirmed']*100/days['confirmed'][-2])
        info['percentageactive']=round(info['diffactive']*100/daily_df['active'].tolist()[-2])
        info['percentagerecovered']=round(info['diffrecovered']*100/days['recovered'][-2])
        info['percentagedeath']=round(info['diffdeath']*100/days['death'][-2])

        cached_data = {
            'statewise': statewise,
            'info': info,
            'days': days,
            'tests': tests
        }

        save_cache(cache_key, cached_data)
        from_cache= 'false'

        
    t2 = time.time()
    compute = t2-t1
    return render(req,'adarsh.html',{
        'data': mark_safe(json.dumps(cached_data)),
        'compute': compute,
        'from_cache': from_cache,
        'dict': cached_data
    })

def ping(req):
    return HttpResponse('<h1>pong</h1>')

#services
def get_mohfw():
    url = "https://www.mohfw.gov.in/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_statewise(soup):
    trows=soup.findAll('tr')


    state=list()
    confirmed=list()
    discharged=list()
    death=list()
    for row in trows:
       # for element in row(text=lambda text: isinstance(text, Comment)):
            #element.extract()
        lst=row.find_all('td')
        if(len(lst)==5):
            try:
                check_state((remove_html_tags(lst[1])))
                state.append((remove_html_tags(lst[1])))
                confirmed.append(get_count(remove_html_tags(lst[2])))
                discharged.append(get_count(remove_html_tags(lst[3])))
                death.append(get_count(remove_html_tags(lst[4])))
            except:
                pass
        else:
            pass
    data=pd.DataFrame(list(zip(state,confirmed,discharged,death)),columns=['state','confirmed','discharged','death'])
    data['active']=data['confirmed']-data['discharged']-data['death']
    data.sort_values(by='confirmed',axis=0,ascending=False,inplace=True)
    statewise = data.to_dict()
    info=dict()

    for ke in statewise:
        statewise[ke]=list(statewise[ke].values())

    return statewise

def get_info(soup):
    counts=soup.findAll("div", {"class": "site-stats-count"})
    info = dict()
    info['infected']=get_count(counts[0].findAll('li')[0].find('strong'))
    info['cured']=get_count(counts[0].findAll('li')[1].find('strong'))
    info['death']=get_count(counts[0].findAll('li')[2].find('strong'))
    info['migrated']=get_count(counts[0].findAll('li')[3].find('strong'))
    info['source'] = 'mohfw'

    url="https://www.worldometers.info/coronavirus/country/india/"
    response=requests.get(url)

    worldo=BeautifulSoup(response.text, "html.parser")
    worldo_counts=worldo.findAll("div",{"class": "maincounter-number"})
    worldo_counts=[get_count(remove_html_tags(x)) for x in worldo_counts]
    labels=['infected','death','cured']
    info2=dict(zip(labels,worldo_counts))

    active=info2['infected']-info2['death']-info2['cured']-int(info['migrated'])
    if(int(info['infected'])>active):
        info['confirmed']=str(int(info['infected'])+int(info['cured'])+int(info['death'])+int(info['migrated']))
        return info
    else:
        info['infected']=str(active)
        info['death']=str(info2['death'])
        info['cured']=str(info2['cured'])
        info['confirmed']=str(info2['infected'])
        info['source'] = 'worldometers'
        return info

def get_wiki():
    wiki_url="https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_India"
    wiki_response=requests.get(wiki_url)
    wiki = BeautifulSoup(wiki_response.text, "html.parser")
    return wiki

def get_daily(wiki,confirmed):
    counts=wiki.findAll("span", {"style":"width:3.5em; padding:0 0.3em 0 0; text-align:right; display:inline-block"})
    dates=wiki.findAll("td",{"colspan":"2","style":"padding-left:0.4em; padding-right:0.4em; text-align:center"})

    lst=list()
    for no in counts:
        try:
            lst.append(get_count(remove_html_tags(no)))
        except:
            pass
    counts=lst

    dates=[remove_html_tags(x) for x in dates]

    daily=dict(zip(dates,counts))
    date=datetime.today()
    date=date.strftime("%Y-%m-%d")
    del daily['⋮']
    del daily['2020-01-30']
    del daily['2020-02-02']
    del daily['2020-02-03']
    daily['2020-03-01']=3
    daily['2020-03-11']=65
    daily[date]=confirmed
    days=dict()
    lst=list()
    for day in sorted(daily):
        d=datetime.strptime(day,"%Y-%m-%d")
        day=d.strftime("%b %d")
        lst.append(day)
    days["date"]=lst
    days["infected"]=sorted(daily.values())
    return days

def get_tests(wiki):
    table = wiki.find("table",{"class":"wikitable plainrowheaders"})
    rows = table.find_all('td')

    tests = {
        "perm":rows[1].text.replace('\n', ''),
        "inds":rows[2].text.replace('\n', '')
    }

    return tests
def check_state(text):
    text=str(text)
    lst=["Andhra Pradesh","Arunachal Pradesh ","Andaman and Nicobar Islands","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Telengana","Ladakh","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","Delhi","Puducherry"]
    if text in lst:
        return text
    else:
        raise Exception("Not a state")


def remove_html_tags(text):
    """Remove html tags from a string"""
    text=str(text)
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def get_count(text):
    text=str(text).replace(",","")
    num=int(re.findall(r'\d+', text)[0])
    return num

def save_cache(key,data):
    try:
        cache = Cache.objects.get(cache_key = key)
        cache.data = json.dumps(data)
    except Cache.DoesNotExist:
        cache = Cache(cache_key = key, data = json.dumps(data))
    cache.save()


def get_cache(key, expiry_time = None):
    try:
        cache = Cache.objects.get(cache_key = key)
        if not expiry_time or cache.updated_at + timezone.timedelta(minutes= expiry_time) > timezone.now():
            return json.loads(cache.data)
    except Cache.DoesNotExist:
        pass


def tweet_update(latest_data):

    consumer_key = CONFIG['consumer_key']
    consumer_secret = CONFIG['consumer_secret']
    access_token = CONFIG['access_token']
    access_token_secret = CONFIG['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth)
    tweet = ("#coronavirusindia  update:\n\n"
            "confirmed cases:  {}\n"
            "active: {}\n"
            "recovered: {}\n"
            "deaths: {}\n\n"
            "Know more: https://coronaindia.ml\n\n"
            "#COVID #COVID19Pandemic "
            "#coronaupdatesindia  #coronavirus "
            "#COVID19outbreak".format(latest_data['confirmed'],latest_data['infected'],latest_data['cured'],latest_data['death']))
    api.update_status(status =tweet)

"""
def tweet(req):
    data={'confirmed':2069,'infected':1860,'cured':155,'death':53}
    tweet_update(data)
    return HttpResponse('<h1>pong</h1>')
"""