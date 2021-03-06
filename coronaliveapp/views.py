
import requests, json, re, urllib.request, time, tweepy, copy

import pandas as pd
from datetime import datetime, date
from bs4 import BeautifulSoup, Comment

from django.http import HttpResponse, JsonResponse, Http404
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.utils import timezone
from coronaliveapp.config import CONFIG
from corona.models import Cache, Daily

from django.urls import reverse

#route functions
def home(req):
    t1 = time.time()

    json_req = req.META['PATH_INFO'] == '/json/'

    cache_key = 'homepage'
    expiry = 5 
    cached_data = get_cache(cache_key, expiry)
    from_cache= 'true'

    if not cached_data:
        try:
            cached_data = get_data_from_covid19org()
            save_cache(cache_key, cached_data)
            from_cache= 'false'
        except Exception as e:
            if json_req:
                raise e
            cached_data = get_cache(cache_key)
    
    if json_req:
        return JsonResponse(cached_data)

    states = []

    for i in  range(len(cached_data['statewise']['state'])):
        states.append({
            'name': cached_data['statewise']['state'][i],
            'confirmed': cached_data['statewise']['confirmed'][i],
            'active': cached_data['statewise']['active'][i],
            'deltaconfirmed' : cached_data['statewise']['deltaconfirmed'][i],
            'deltadeaths' : cached_data['statewise']['deltadeaths'][i],
            'deltarecovered' : cached_data['statewise']['deltarecovered'][i],
            'discharged': cached_data['statewise']['discharged'][i],
            'death': cached_data['statewise']['death'][i],
            'urlkey': cached_data['statewise']['urlkey'][i],
        })

    data_dict = copy.deepcopy(cached_data)
    data_dict['envCfg'] = get_env_cfg()

    t2 = time.time()
    compute = t2-t1
    
    return render(req,'home.html',{
        'data': mark_safe(json.dumps(cached_data)),
        'compute': compute,
        'from_cache': from_cache,
        'dict': data_dict,
        'states': states,
        'type' : 'India',
        'url' : "https://www.coronaindia.ml/"
    })

def statewise_timeline(req):

    cache_key = 'statewise_timeline'
    expiry = 60
    cached_data = get_cache(cache_key, expiry)

    if not cached_data:
        try:
            url = 'https://api.covid19india.org/data.json'
            country_json = requests.get(url).json()

            statewise_dataframe = pd.DataFrame(country_json['statewise'])
            statenames = statewise_dataframe[['state','statecode']]
            statenames['statecode'] = statenames['statecode'].apply(str.lower)

            ### Statewise timeline
            state_daily_url = "https://api.covid19india.org/states_daily.json"
            statewise_timeline = requests.get(state_daily_url).json()
            statewise_df = pd.DataFrame(statewise_timeline['states_daily'])
            statewise_confirmed_df = statewise_df[statewise_df['status']=="Confirmed"]
            statewise_confirmed_df.drop('status',axis=1,inplace=True)
            statewise_confirmed_df.reset_index(inplace=True)
            dates = statewise_confirmed_df['date']
            statewise_confirmed_df.drop('date',axis=1,inplace=True)

            for col in statewise_confirmed_df.columns:
                statewise_confirmed_df[col] = statewise_confirmed_df[col].apply(get_count_state)
            statwise_cummulative_df = statewise_confirmed_df
            for i in range(1,len(statewise_confirmed_df)):
                statwise_cummulative_df.iloc[i]=statwise_cummulative_df.iloc[i]+statwise_cummulative_df.iloc[i-1]
            statwise_cummulative_df.drop('index',axis=1,inplace=True)
            
            statenames.set_index(['statecode'],inplace=True)
            statenames = statenames.to_dict()['state']
            statwise_cummulative_df.rename(columns=statenames,inplace=True)
            dates = [datetime.strptime(x,'%d-%b-%y') for x in dates]
            dates = [x.strftime("%b %d") for x in dates]
            statwise_cummulative_df['date'] = dates

            statewise_daily = {}

            for col in statwise_cummulative_df.columns:
                statewise_daily[col] = statwise_cummulative_df[col].tolist()
            
            cached_data = statewise_daily
            save_cache(cache_key, cached_data)
        except Exception as e:
            cached_data = get_cache(cache_key)
    return JsonResponse(cached_data)

#route functions
def adarsh(req):
    t1 = time.time()
    cache_key = 'adarsh'
    expiry = 5 
    cached_data = get_cache(cache_key, expiry)
    from_cache= 'true'

    if True or not cached_data:



        url = 'https://api.covid19india.org/data.json'
        country_json = requests.get(url).json()


        statewise_dataframe = pd.DataFrame(country_json['statewise'])

        present_data = statewise_dataframe[statewise_dataframe['state']=='Total']

        info = {
            'active' : format_as_indian(int(present_data['active'].sum())),
            'confirmed' : int(present_data['confirmed'].sum()),
            'death' : int(present_data['deaths'].sum()),
            'recovered' : int(present_data['recovered'].sum())
        }

        statewise_dataframe = statewise_dataframe[1:]
        statewise_dataframe = statewise_dataframe[statewise_dataframe['confirmed']!='0']

        statewise = {
            'state' : statewise_dataframe['state'].tolist(),
            'statecode' : statewise_dataframe['statecode'].apply(str.lower).tolist(),
            'active' : statewise_dataframe['active'].apply(int).tolist(),
            'confirmed':statewise_dataframe['confirmed'].apply(int).tolist(),
            'death' : statewise_dataframe['deaths'].apply(int).tolist(),
            'discharged' : statewise_dataframe['recovered'].apply(int).tolist()
        }

        daily_dataframe = pd.DataFrame(country_json['cases_time_series'])

        days = {
            'date' : daily_dataframe['date'].tolist(),
            'confirmed' : daily_dataframe['totalconfirmed'].apply(int).tolist(),
            'recovered' : daily_dataframe['totalrecovered'].apply(int).tolist(),
            'death' : daily_dataframe['totaldeceased'].apply(int).tolist(),
            'confirmedincrease' : daily_dataframe['dailyconfirmed'].apply(int).tolist(),
            'recoveredincrease' : daily_dataframe['dailyrecovered'].apply(int).tolist(),
            'deathincrease' : daily_dataframe['dailydeceased'].apply(int).tolist()
        }

        
        info = get_info_details(info,days)

        
        tests={1:1,2:2}

        cached_data = {
            'statewise': statewise,
            'info': info,
            'days': days,
            'tests': tests
        }

        save_cache(cache_key, cached_data)
        from_cache= 'false'

    data_dict = cached_data
    data_dict['envCfg'] = get_env_cfg()

    t2 = time.time()
    compute = t2-t1
    return render(req,'adarsh.html',{
        'data': mark_safe(json.dumps(cached_data)),
        'compute': compute,
        'from_cache': from_cache,
        'dict': data_dict
    })

def stateupdate(req):
    t1 = time.time()

    raw_uri = req.META['PATH_INFO']
    state_name = raw_uri.replace('/','').replace('-coronavirus-updates','').replace('-', ' ')

    data = get_state_data(state_name)

    if data == 'STATE_NOT_FOUND':
        raise Http404()
    from_cache= 'false'
    
    states = []
    for i in  range(len(data['statewise']['state'])):
        states.append({
            'name': data['statewise']['state'][i],
            'confirmed': data['statewise']['confirmed'][i],
            'active': data['statewise']['active'][i],
            'discharged': data['statewise']['recovered'][i],
            'death': data['statewise']['death'][i],
            'deltaconfirmed' : data['statewise']['deltaconfirmed'][i],
            'deltarecovered' : data['statewise']['deltarecovered'][i],
            'deltadeaths' : data['statewise']['deltadeath'][i]
        })

    t2 = time.time()
    compute = t2-t1

    
    return render(req,'districtwise.html',{
        'data': mark_safe(json.dumps(data)),
        'compute': compute,
        'from_cache': from_cache,
        'dict': data,
        'states' : states,
        'type' : data['type'],
        'url' : "https://www.coronaindia.ml"+raw_uri
    })


def ping(req):
    meta = req.META['RAW_URI']
    #js = json.dumps(meta)
    #path = str(reverse(viewname='ping'))
    return HttpResponse('<h1>pong: '+ meta +'</h1>')

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
    try:
        num=int(re.findall(r'\d+', text)[0])
        return num
    except :
        return 0

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
            "#COVID19outbreak".format(latest_data['confirmed'],latest_data['active'],latest_data['recovered'],latest_data['death']))
    api.update_status(status =tweet)


def tweet(req):
    data={'confirmed':2069,'infected':1860,'cured':155,'death':53}
    tweet_update(data)
    return HttpResponse('<h1>pong</h1>')




def get_state_data(state_name):
    url = 'https://api.covid19india.org/data.json'

    country_json = requests.get(url).json()

    statewise_dataframe = pd.DataFrame(country_json['statewise'])
    
    statewise_dataframe['state_key'] = statewise_dataframe['state'].apply(str.lower)

    present_data = statewise_dataframe[statewise_dataframe['state_key']== state_name]

    state_name = present_data['state'].sum()
    
    if not state_name:
        return 'STATE_NOT_FOUND'
    
    state_code = present_data['statecode'].sum().lower()

    info = get_info_details(present_data)

    state_daily_url = "https://api.covid19india.org/states_daily.json"
    statewise_json_url = 'https://api.covid19india.org/state_district_wise.json'

    statewise_timeline = requests.get(state_daily_url).json()
    changes = statewise_timeline['states_daily']


    dates = []
    for change in changes:
        if(change['status']=='Confirmed'):
            dates.append(change['date'])

    confirmedincrease = []
    recoveredincrease = []
    deathincrease = []
    confirmed = []
    recovered = []
    death = []
    
    #### Date format
    dates = [datetime.strptime(x,'%d-%b-%y') for x in dates]
    dates = [x.strftime("%b %d") for x in dates]
    
    for change in changes:
        if(change['status']=='Confirmed'):
            confirmedincrease.append(get_count(change[state_code]))
        if(change['status']=='Recovered'):
            recoveredincrease.append(get_count(change[state_code])) 
        if(change['status']=='Deceased'):
            deathincrease.append(get_count(change[state_code]))

    for i in range(1,len(confirmedincrease)+1):
        confirmed.append(sum(confirmedincrease[0:i]))
        recovered.append(sum(recoveredincrease[0:i]))
        death.append(sum(deathincrease[0:i]))


    active = [confirmed[i]-recovered[i]-death[i] for i in range(len(confirmed))]
    activeincrease = [active[0]]

    for i in range(1,len(active)):
        activeincrease.append(active[i]-active[i-1])

    previous = -30
    days = {
        'date' : dates[previous:],
        'confirmed' : confirmed[previous:],
        'recovered' : recovered[previous:],
        'death' : death[previous:],
        'active' : active[previous:],
        'confirmedincrease' : confirmedincrease[previous:],
        'recoveredincrease' : recoveredincrease[previous:],
        'deathincrease' : deathincrease[previous:],
        'activeincrease' : activeincrease[previous:]
    }

    statewise_json = requests.get(statewise_json_url).json()

    state = statewise_json[state_name]

    districts = []
    confirmed = []
    recovered = []
    death = []
    deltaconfirmed = []
    deltarecovered = []
    deltadeath = []

    for district in state['districtData']:
        districts.append(district)
        confirmed.append(state['districtData'][district]['confirmed'])
        recovered.append(state['districtData'][district]['recovered'])
        death.append(state['districtData'][district]['deceased'])
        deltaconfirmed.append(state['districtData'][district]['delta']['confirmed'])
        deltarecovered.append(state['districtData'][district]['delta']['recovered'])
        deltadeath.append(state['districtData'][district]['delta']['deceased'])
        

    data=pd.DataFrame(zip(districts,confirmed,recovered, death,deltaconfirmed,deltarecovered,deltadeath),columns=['state','confirmed','recovered','death','deltaconfirmed','deltarecovered','deltadeath'])
    data.sort_values(by=['confirmed'],axis=0,inplace=True,ascending=False)
    data['active'] = data['confirmed']-data['death']-data['recovered']
    statewise = {
        'state' : data['state'].tolist(),
        'confirmed' : data['confirmed'].tolist(),
        'recovered' : data['recovered'].tolist(),
        'active' : data['active'].tolist(),
        'death' : data['death'].tolist(),
        'deltadeath' : data['deltadeath'].tolist(),
        'deltarecovered' : data['deltarecovered'].tolist(),
        'deltaconfirmed' : data['deltaconfirmed'].tolist()
    }

    tests = None
    ## Zones
    r = requests.get('https://api.covid19india.org/zones.json')
    r = r.json()['zones']
    df = pd.DataFrame(r)
    state_df = df[df['state']==state_name]
    green = state_df['district'][state_df['zone']=='Green']
    orange = state_df['district'][state_df['zone']=='Orange']
    red = state_df['district'][state_df['zone']=='Red']
    zones = {
        "red" : red.tolist(),
        "green" : green.tolist(),
        "orange" : orange.tolist()
    }

    data = {
        'statewise': statewise,
        'info': info,
        'days': days,
        'tests': tests,
        'type' : state_name,
        'zone' : zones
    }

    return data

    


def get_statename(text):
    try:
        url = 'https://api.covid19india.org/data.json'
        country_json = requests.get(url).json()

        statewise_dataframe = pd.DataFrame(country_json['statewise'])
        
        states = statewise_dataframe['state'].tolist()
        raw_states = statewise_dataframe['state'].apply(str.lower).tolist()
        statecode = statewise_dataframe['statecode'].apply(str.lower).tolist()

        for i in range(len(raw_states)):
            raw_states[i] = raw_states[i].replace(" ",'')

        details = list(zip(states,statecode))
        raw = dict(zip(raw_states,details))
        
        text = str(text).lower()
        state = (re.findall(r'\w+', text)[0])
        lst = raw[state]
        print(lst)
    except:
        raise Http404()
    return lst


def get_info_details(present_data):
    info = {
        'active' : int(present_data['active'].sum()),
        'confirmed' : int(present_data['confirmed'].sum()),
        'death' : int(present_data['deaths'].sum()),
        'recovered' : int(present_data['recovered'].sum()),
        'diffconfirmed' : int(present_data['deltaconfirmed'].sum()),
        'diffdeath' : int(present_data['deltadeaths'].sum()),
        'diffrecovered' : int(present_data['deltarecovered'].sum()),
        'diffactive' : int(present_data['deltaconfirmed'].sum())-int(present_data['deltadeaths'].sum())-int(present_data['deltarecovered'].sum())
    }
    if(info['diffconfirmed']==0):
        info['percentageconfirmed']=0
    elif((info['confirmed']-info['diffconfirmed'])==0):
        info['percentageconfirmed']=""
    else:
        info['percentageconfirmed']=int((info['diffconfirmed']*100)/(info['confirmed']-info['diffconfirmed']))
    
    if(info['diffrecovered']==0):
        info['percentagerecovered']=0
    elif((info['recovered']-info['diffrecovered'])==0):
        info['percentagerecovered']=""
    else:
        info['percentagerecovered']=int((info['diffrecovered']*100)/(info['recovered']-info['diffrecovered']))
    
    if(info['diffdeath']==0):
        info['percentagedeath']=0
    elif((info['death']-info['diffdeath'])==0):
        info['percentagedeath']=""
    else:    
        info['percentagedeath']=int((info['diffdeath']*100)/(info['death']-info['diffdeath']))
    
    if(info['diffactive']==0):
        info['percentageactive']=0
    elif((info['active']-info['diffactive'])==0):
        info['percentageactive']=""
    else:
        info['percentageactive']=int(abs((info['diffactive']*100)/(info['active']-info['diffactive'])))
    ####
    
    return info

def get_scraped_data():
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

    return {
        'statewise': statewise,
        'info': info,
        'days': days,
        'tests': tests,
    }

def get_urlkey(string):
    return string.strip().replace(' ','-').lower()

def get_data_from_covid19org():
    url = 'https://api.covid19india.org/data.json'


    ## Tests
    country_json = requests.get(url).json()
    tests=pd.DataFrame(country_json['tested'])
    test = tests['totalsamplestested'].tolist()
    totaltests = max(list(map(get_count,test)))

    statewise_dataframe = pd.DataFrame(country_json['statewise'])

    present_data = statewise_dataframe[statewise_dataframe['state']=='Total']

    statewise_dataframe['urlkey'] = statewise_dataframe['state'].apply(get_urlkey)

    info = get_info_details(present_data)
    
    ## for statewise timeline
    statenames = statewise_dataframe[['state','statecode']]
    statenames['statecode'] = statenames['statecode'].apply(str.lower)

    statewise_dataframe = statewise_dataframe[1:]
    statewise_dataframe['confirmed'] = statewise_dataframe['confirmed'].apply(int)
    statewise_dataframe = statewise_dataframe[statewise_dataframe['confirmed'] != 0]
    statewise_dataframe.sort_values(by=['confirmed'], inplace=True, ascending = False)
    #statewise_dataframe.sort_values(by=['confirmed'], inplace=True, asending = False)

    statewise = {
        'state' : statewise_dataframe['state'].tolist(),
        'statecode' : statewise_dataframe['statecode'].apply(str.lower).tolist(),
        'active' : statewise_dataframe['active'].apply(int).tolist(),
        'confirmed':statewise_dataframe['confirmed'].apply(int).tolist(),
        'deltaconfirmed' : statewise_dataframe['deltaconfirmed'].apply(int).tolist(),
        'deltadeaths' : statewise_dataframe['deltadeaths'].apply(int).tolist(),
        'deltarecovered' : statewise_dataframe['deltarecovered'].apply(int).tolist(),
        'death' : statewise_dataframe['deaths'].apply(int).tolist(),
        'discharged' : statewise_dataframe['recovered'].apply(int).tolist(),
        'urlkey': statewise_dataframe['urlkey'].tolist()
    }

    daily_dataframe = pd.DataFrame(country_json['cases_time_series'])
    daily_dataframe = daily_dataframe.tail(30)
    daily_dataframe['fulldate'] = daily_dataframe['date'].apply(lambda d: datetime.strptime(d+'2020','%d %B %Y'))
    daily_dataframe['date'] = daily_dataframe['fulldate'].apply(lambda d: datetime.strftime(d,'%b %d'))
    days = {
        'date' : daily_dataframe['date'].tolist(),
        'confirmed' : daily_dataframe['totalconfirmed'].apply(int).tolist(),
        'recovered' : daily_dataframe['totalrecovered'].apply(int).tolist(),
        'death' : daily_dataframe['totaldeceased'].apply(int).tolist(),
        'confirmedincrease' : daily_dataframe['dailyconfirmed'].apply(int).tolist(),
        'recoveredincrease' : daily_dataframe['dailyrecovered'].apply(int).tolist(),
        'deathincrease' : daily_dataframe['dailydeceased'].apply(int).tolist()
    }
    
    tests = {
        'samples' : format_as_indian(totaltests),
        'perMillion': format_as_indian(totaltests//1300)
    }



    return {
        'statewise': statewise,
        'info': info,
        'days': days,
        'tests': tests,
        'type' : 'India'
    }

def get_env_cfg():
    beta = CONFIG.get('ENV') == 'BETA'
    debug = CONFIG.get('DEBUG', False)
    return {
        'beta': beta,
        'debug': debug
    }



def format_as_indian(input):
    input_list = list(str(input))
    if len(input_list) <= 1:
        formatted_input = input
    else:
        first_number = input_list.pop(0)
        last_number = input_list.pop()
        formatted_input = first_number + (
            (''.join(l + ',' * (n % 2 == 1) for n, l in enumerate(reversed(input_list)))[::-1] + last_number)
        )

        if len(input_list) % 2 == 0:
            formatted_input.lstrip(',')

    return formatted_input



def get_count_state(num):
    try:
        return int(num)
    except:
        return 0