from .models import Langing


import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe
import vk_api
import time
import datetime

from rq import Queue
from worker import conn
from utils import analitica,colvodneyforday


from conecttosheets import connectsheet,connectIP,connect

def googlesheets(completeurl):
    df=connect(completeurl)
    df['new_col'] = df['utm_source'] + ' / ' + df['utm_medium']
    a = df.dropna(subset=[list(df)[0]])
    newdf = a[['utm_source', 'utm_medium', 'utm_campaign', 'new_col']]
    slovaritog = {'Уникальная': 0, 'Дайджест': 0, 'SMM репостов': 0,
                  'Инфопартнеры':0, 'Рассылка из юнисендера': 0, 'Промо в вузах': 0, 'Телеграм': 0,
                  'Таргетинг': 0,
                  'Веб-страница и слайдер': 0, 'Контекстная реклама': 0, 'Органика и неопознанный трафик': 0}
    for i in list(newdf['new_col']):
        ii = str(i)
        if 'generalbase' in ii or 'mailchimp' in ii:
            slovaritog['Уникальная'] += 1
        elif 'digest' in ii or 'Digest' in ii:
            slovaritog['Дайджест'] += 1
        elif 'vk-wall' in ii or 'vk_wall' in ii:
            slovaritog['SMM репостов'] += 1
        elif 'ip-' in ii or 'ip_' in ii:
            slovaritog['Инфопартнеры'] += 1
        elif 'mail' in ii or 'email' in ii or 'Unisender' in ii or 'unisender' in ii or 'utm_source' in ii or 'UniSender' in ii:
            slovaritog['Рассылка из юнисендера'] += 1
        elif 'vuz-' in ii or 'vuz_' in ii:
            slovaritog['Промо в вузах'] += 1
        elif 'tg /' in ii or 'Tg /' in ii:
            slovaritog['Телеграм'] += 1
        elif 'vk / target' in ii or 'vk / targetpost' in ii or 'vk / target-story' in ii or 'insta / target' in ii or 'insta / targetpost' in ii or 'insta / target-story' in ii or 'fb / target' in ii or 'fb / targetpost' in ii:
            slovaritog['Таргетинг'] += 1
        elif 'cl-site' in ii or 'Сl-site' in ii or 'cl_site' in ii or 'Сl_site' in ii:
            slovaritog['Веб-страница и слайдер'] += 1
        elif 'google / cpc' in ii or 'youtube / instream' in ii or 'yandex / cpc' in ii:
            slovaritog['Контекстная реклама'] += 1
        else:
            slovaritog['Органика и неопознанный трафик'] += 1

    return slovaritog

def infopartnerip(urlland):
    dfip=connectIP('https://docs.google.com/spreadsheets/d/1WmDnz3794uoU_h7ho_hOPMISUA2CdXt_UA_8L9pcJ-s/edit?pli=1#gid=0')
    costdf = dfip[dfip.values == urlland].loc[:, 'Стоимость ']
    ipKOLICHESTVO = len(costdf)
    sumcostdf = 0
    for i in costdf.index:
        sumcostdf += int(costdf[i])
    return [ipKOLICHESTVO,sumcostdf]

def SMMcountfunct(start,stop,heshteg):
    s1 = start[-2:] + '/' + start[-5:-3] + '/' + start[0:4]
    unixtime1 = time.mktime(datetime.datetime.strptime(s1, "%d/%m/%Y").timetuple())
    s2 = stop[-2:] + '/' + stop[-5:-3] + '/' + stop[0:4]
    unixtime2 = time.mktime(datetime.datetime.strptime(s2, "%d/%m/%Y").timetuple())
    vk_session = vk_api.VkApi('+79055106387', '#rr7363446909250797rr##')
    vk_session.auth()

    vk = vk_session.get_api()
    SMMM = vk.wall.search(owner_id=-25758, query=heshteg, count=100)
    newwww = []
    for i in range(len(SMMM['items'])):
        if SMMM['items'][i]['date'] > int(unixtime1) and SMMM['items'][i]['date'] < int(unixtime2):
            newwww.append(SMMM['items'][i]['id'])
    idreposts = []
    for i in newwww:
        slova = vk.wall.getReposts(owner_id=-25758, post_id=i, count=1000)
        for i in range(len(slova['items'])):
            if slova['items'][i]['from_id'] < 0:
                idreposts.append(slova['items'][i]['from_id'])

    return len(idreposts)

def main():
    landing = Langing.objects.all()
    dictItog={}


    q = Queue(connection=conn)
    q1 = Queue(connection=conn)
    q2 = Queue(connection=conn)
    
    #q2targeting = Queue(connection=conn)
    result = q.enqueue(analitica,str(landing[0].land),str(landing[0].success),str(landing[0].start),str(landing[0].end),str(landing[0].complete))
    result1 = q1.enqueue(colvodneyforday,str(landing[0].start),str(landing[0].end),str(landing[0].land))
    try:
        connecttocomplete = googlesheets(str(landing[0].complete))
    except:
        pass
    try:
        result2 = connectsheet('https://docs.google.com/spreadsheets/d/1lcHMPIw1AtzKx3DoFAVp_JDi2Cb_-DbP9krjtD7c69Q/edit#gid=237212384',str(landing[0].start),str(landing[0].land))
    except:
        pass

    try:
        infopartenrilist=infopartnerip('https://1.changellenge.com/supply-chain')
    except:
        pass
    SMMcount=SMMcountfunct(str(landing[0].start),str(landing[0].end),str(landing[0].heshteg))
    #time.sleep(5)
    print("REZULT"*100)
    print(result.result)
    print(result1.result)
    print(result2)
    print(infopartenrilist)
    print(SMMcount)
    print(connecttocomplete)
    
    dictItog=result.result
    connecttocompleteresult=connecttocomplete
    if bool(connecttocompleteresult) ==True:
        regfactnomer=0
        for i in dictItog['Источник']:
            dictItog['Регистрациифакт'][regfactnomer]=connecttocompleteresult[i]
            regfactnomer+=1
    else:
        pass
    try:
        dictItog['Количество'][7]=result1.result[0]
    except:
        pass
    try:
        dictItog['Количество'][8]=result1.result[1]
    except:
        pass
    try:
        dictItog['Количество'][9]=result1.result[2]
    except:
        pass
    try:
        dictItog['Количество'][0]=result1.result[3]
    except:
        pass
    try:
        dictItog['Количество'][1]=result1.result[4]
    except:
        pass
    try:
        dictItog['Количество'][6]=result1.result[5]
    except:
        pass
    try:
        dictItog['Трафикфакт'][7]=result2['Трафикфакт']
    except:
        pass
    try:
        dictItog['Бюджетплан'][7]=result2['Бюджетплан']
    except:
        pass
    try:
        dictItog['Бюджетфакт'][7]=result2['Бюджетфакт']
    except:
        pass
    try:
        dictItog['Количество'][3]=infopartenrilist[0]
    except:
        pass
    try:
        dictItog['Бюджетфакт'][3]=infopartenrilist[1]
    except:
        pass
    try:
        dictItog['Количество'][2]=SMMcount
    except:
        pass
    a=[]
    for i in range(len(dictItog['Трафикфакт'])):
        if int(dictItog['Количество'][i])!=0:
            a.append(int(int(dictItog['Трафикфакт'][i]) / int(dictItog['Количество'][i])))
        else:
            a.append('—')
    dictItog["Сила"]=a
    print(dictItog)
                           
    return dictItog
if __name__ == "__main__":
    # execute only if run as a script
    main()
