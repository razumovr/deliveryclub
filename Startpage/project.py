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


    q = Queue(connection=conn)
    q1 = Queue(connection=conn)
    #q2targeting = Queue(connection=conn)
    result = q.enqueue(analitica,str(landing[0].land),str(landing[0].success),str(landing[0].start),str(landing[0].end),str(landing[0].complete))
    result1 = q1.enqueue(colvodneyforday,str(landing[0].start),str(landing[0].end),str(landing[0].land))
    #result2 = q2targeting.enqueue(connectsheet,'https://docs.google.com/spreadsheets/d/1lcHMPIw1AtzKx3DoFAVp_JDi2Cb_-DbP9krjtD7c69Q/edit#gid=237212384',str(landing[0].start),str(landing[0].land))
    result2 = connectsheet('https://docs.google.com/spreadsheets/d/1lcHMPIw1AtzKx3DoFAVp_JDi2Cb_-DbP9krjtD7c69Q/edit#gid=237212384',str(landing[0].start),str(landing[0].land))

    try:
        infopartenrilist=infopartnerip('https://1.changellenge.com/supply-chain')
        '''d['Количество'][3] = infopartenrilist[0]
        d['Бюджетфакт'][3] = infopartenrilist[1]'''
    except:
        pass
    SMMcount=SMMcountfunct(start,stop,str(landing[0].heshteg))
    time.sleep(15)
    print("REZULT"*100)
    print(result.result)
    print(result1.result)
    print(result2)
    print(infopartenrilist)
    print(SMMcount)
                                 
                        
    return result.result
if __name__ == "__main__":
    # execute only if run as a script
    main()
