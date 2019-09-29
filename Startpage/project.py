from .models import Langing
from .conecttosheets import connect,connectsheet,connectIP
from .utils import analitica




import pandas as pd


import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe
import vk_api
import time

from rq import Queue
from worker import conn







def tabletargeting(datastart):
    '''scope = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '/Users/ruslan/Downloads/My Project-fe4805e9d102.json', scope)
    gc = gspread.authorize(credentials)
    targetsht = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1lcHMPIw1AtzKx3DoFAVp_JDi2Cb_-DbP9krjtD7c69Q/edit#gid=237212384').get_worksheet(
        17)
    df = get_as_dataframe(targetsht, header=0)'''
    df=connectsheet('https://docs.google.com/spreadsheets/d/1lcHMPIw1AtzKx3DoFAVp_JDi2Cb_-DbP9krjtD7c69Q/edit#gid=237212384',datastart)
    return df

def infopartnerip(urlland):
    '''scope = ['https://www.googleapis.com/auth/drive', 'https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        '/Users/ruslan/Downloads/My Project-fe4805e9d102.json', scope)
    gc = gspread.authorize(credentials)
    ippartner = gc.open_by_url(
        'https://docs.google.com/spreadsheets/d/1WmDnz3794uoU_h7ho_hOPMISUA2CdXt_UA_8L9pcJ-s/edit?pli=1#gid=0').sheet1
    dfip = get_as_dataframe(ippartner, header=0)'''
    #Sortirovat po datam dock Kris
    #start2=datetime.date(int(start[:4]), int(start[5:7]), int(start[8:10]))
    #stop2=datetime.date(int(stop[:4]), int(stop[5:7]), int(stop[8:10]))
    dfip=connectIP('https://docs.google.com/spreadsheets/d/1WmDnz3794uoU_h7ho_hOPMISUA2CdXt_UA_8L9pcJ-s/edit?pli=1#gid=0')
    costdf = dfip[dfip.values == urlland].loc[:, 'Стоимость ']
    ipKOLICHESTVO = len(costdf)
    sumcostdf = 0
    for i in costdf.index:
        sumcostdf += int(costdf[i])
    return [ipKOLICHESTVO,sumcostdf]



'''def kolvopicsfunct(k):
    unikalkarry = []
    digestarray = []
    telegaarray = []
    # lif 'digest' in i or 'Digest' in i:
    #  elif 'tg /' in i or 'Tg /' in i:
    for i in range(len(k)):
        for j in range(len(k[i])):
            if 'generalbase' in str(k[i][j]) or 'mailchimp' in str(k[i][j]):
                unikalkarry.append(k[i][j + 1])
            elif 'digest' in str(k[i][j]) or 'Digest' in str(k[i][j]):
                digestarray.append(k[i][j + 1])
            elif 'tg /' in str(k[i][j]) or 'Tg /' in str(k[i][j]):
                telegaarray.append(k[i][j + 1])
            else:
                pass
    #  if 'generalbase' in ii or 'mailchimp' in ii:

    max_value = 0
    for n in unikalkarry:
        if n > max_value:
            max_value = n
    if max_value == 1:
        lenUNIKALKA = sg.find_peaks_cwt(unikalkarry, np.arange(1, int(max_value + 1)),
                                        max_distances=np.arange(1, int(max_value + 1)))
    elif max_value == 0:
        lenUNIKALKA = []
    else:
        lenUNIKALKA = sg.find_peaks_cwt(unikalkarry, np.arange(1, int(max_value)),
                                        max_distances=np.arange(1, int(max_value)))

    max_value = 0
    for n in digestarray:
        if n > max_value:
            max_value = n
    if max_value == 1:
        lenDIGEST = sg.find_peaks_cwt(digestarray, np.arange(1, int(max_value + 1)),
                                      max_distances=np.arange(1, int(max_value + 1)))
    elif max_value == 0:
        lenDIGEST = []
    else:
        lenDIGEST = sg.find_peaks_cwt(digestarray, np.arange(1, int(max_value)),
                                      max_distances=np.arange(1, int(max_value)))

    max_value = 0
    for n in telegaarray:
        if n > max_value:
            max_value = n
    if max_value == 1:
        lenTELEGA = sg.find_peaks_cwt(telegaarray, np.arange(1, int(max_value + 1)),
                                      max_distances=np.arange(1, int(max_value + 1)))
    elif max_value == 0:
        lenTELEGA = []
    else:
        lenTELEGA = sg.find_peaks_cwt(telegaarray, np.arange(1, int(max_value)),
                                      max_distances=np.arange(1, int(max_value)))



    return [len(lenUNIKALKA),len(lenDIGEST),len(lenTELEGA)]'''




def main():
    landing = Langing.objects.all()
    #Langing.objects.all()
    #from .models import Langing

    #d=analitica(landing)

    q = Queue(connection=conn)
    result = q.enqueue(analitica,landing)
    print("Helow"*100)
    print(result.result)
    time.sleep(15)
    print(result.result)  






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
    return d
if __name__ == "__main__":
    # execute only if run as a script
    main()
