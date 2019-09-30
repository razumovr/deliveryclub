from .models import Langing


import pandas as pd


import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe
import vk_api
import time

from rq import Queue
from worker import conn
from utils import analitica,hellow,colvodneyforday


from conecttosheets import connect,connectsheet,connectIP



def infopartnerip(urlland):
    dfip=connectIP('https://docs.google.com/spreadsheets/d/1WmDnz3794uoU_h7ho_hOPMISUA2CdXt_UA_8L9pcJ-s/edit?pli=1#gid=0')
    costdf = dfip[dfip.values == urlland].loc[:, 'Стоимость ']
    ipKOLICHESTVO = len(costdf)
    sumcostdf = 0
    for i in costdf.index:
        sumcostdf += int(costdf[i])
    return [ipKOLICHESTVO,sumcostdf]

def main():
    landing = Langing.objects.all()


    q = Queue(connection=conn)
    q1 = Queue(connection=conn)
    #q2targeting = Queue(connection=conn)
    result = q.enqueue(analitica,str(landing[0].land),str(landing[0].success),str(landing[0].start),str(landing[0].end),str(landing[0].complete))
    result1 = q1.enqueue(colvodneyforday,str(landing[0].start),str(landing[0].end),str(landing[0].land))
    #result2 = q2targeting.enqueue(connectsheet,'https://docs.google.com/spreadsheets/d/1lcHMPIw1AtzKx3DoFAVp_JDi2Cb_-DbP9krjtD7c69Q/edit#gid=237212384',str(landing[0].start),str(landing[0].land))
    result2 = connectsheet('https://docs.google.com/spreadsheets/d/1lcHMPIw1AtzKx3DoFAVp_JDi2Cb_-DbP9krjtD7c69Q/edit#gid=237212384',str(landing[0].start),str(landing[0].land))

    try:
        infopartenrilist=infopartnerip('https://1.changellenge.com/supply-chain'))
        '''d['Количество'][3] = infopartenrilist[0]
        d['Бюджетфакт'][3] = infopartenrilist[1]'''
    except:
        pass
    time.sleep(20)
    print("REZULT"*100)
    print(result.result)
    print(result1.result)
    print(result2)
    print(infopartenrilist)
                                 
                         
    
    '''time.sleep(2)
    print(result.result)
    time.sleep(2)
    print(result.result) 
    time.sleep(2)
    print(result.result) 
    time.sleep(2)
    print(result.result)
    time.sleep(2)
    print(result.result) 
    time.sleep(2)
    print(result.result) 
    time.sleep(2)
    print(result.result)
    time.sleep(2)
    print(result.result) 
    time.sleep(2)
    print(result.result)'''






    '''vuz = 0
    set_data_valuestraf = set(data_namestraf)
    for i in set_data_valuestraf:
        if 'vuz-' in i or 'vuz_' in i:
            vuz += 1'''
    '''
    d['Количество'][5] = vuz'''

    '''colvodneylist=colvodneyforday(start,stop,service,urltoLanding)
    d['Количество'][7] = colvodneylist[0]
    d['Количество'][8] = colvodneylist[1]
    d['Количество'][9] = colvodneylist[2]


    sheet=tabletargeting(start)
    for i in range(len(sheet['Проект'])):
        if sheet['Ссылка на лендинг'][i] == str(landing[0].land):
            d['Трафикфакт'][7] = sheet['Клики факт'][i]
            d['Бюджетплан'][7] = sheet['Бюджет план'][i]
            d['Бюджетфакт'][7] = sheet['Бюджет факт'][i]
            d['Конверсия'][7] = str(int((int(d['Регистрациифакт'][7]) / int(d['Трафикфакт'][7])* 100)))+'%'
        else:
            pass'''
    #d['Конверсия'][7] = str(int(int(d['Регистрациифакт'][7]) / float(d['Трафикфакт'][7] * 100))) + '%'

    '''if str(df['Клики факт'][12])[0] == '=':
        d['Трафикфакт'][7] = eval(df['Клики факт'][12][1:])
    else:
        d['Трафикфакт'][7] = df['Клики факт'][12]

    if str(df['Бюджет план'][12])[0] == '=':
        d['Бюджетплан'][7] = eval(df['Бюджет план'][12][1:])
    else:
        d['Бюджетплан'][7] = df['Бюджет план'][12]

    if str(df['Бюджет факт'][12])[0] == '=':
        d['Бюджетфакт'][7] = eval(df['Бюджет факт'][12][1:])
    else:
        d['Бюджетфакт'][7] = df['Бюджет факт'][12]
    d['Конверсия'][7] = str(int(d['Регистрациифакт'][7] / d['Трафикфакт'][7] * 100)) + '%'''

    '''try:
        infopartenrilist=infopartnerip(str(landing[0].land))
        d['Количество'][3] = infopartenrilist[0]
        d['Бюджетфакт'][3] = infopartenrilist[1]
    except:
        pass'''




    '''kolvopics=kolvopicsfunct(colvodneylist[3])
    d['Количество'][0] = kolvopics[0]
    d['Количество'][1] = kolvopics[1]
    d['Количество'][6] = kolvopics[2]'''
    return result.result
if __name__ == "__main__":
    # execute only if run as a script
    main()
