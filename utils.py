client_id = '1063016171261-3m0ntr3asvduesaail3o4qh35kq8dc5e.apps.googleusercontent.com'
client_secret= '1Iq9izwrNSrH3ASq5zAQmBPt'
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
access_code = '4/igElgTbVX0AEwotwcMC-3jB0haCNjAeIrNgSZxWpv6DXVk21ziI_C8Q'
access_token = 'ya29.GltJB_64t5BuEef6aL25xprUf8Za7DXIIBAKBWvd5fQvI6AVkiYDQo6ZFrl7A_MEPCgn3S3R5tcpJXifAvPDNYOMYA6iUITKY5fEBb6CiIuX1Do3oBsya7W-Fp1B'
refresh_token = '1/a3fH-ISLUlVyz115g7Kp2REoPt0s-KqHUoxKv0vr18g'
#ANALITICA
import httplib2
from oauth2client.client import OAuth2WebServerFlow, GoogleCredentials
from googleapiclient.discovery import build
import datetime
import pandas as pd
#ENDANALITICA
import re
import itertools
#####COLVO
from datetime import date, timedelta
##PICS
import scipy.signal as sg
import numpy as np

from .conecttosheets import connect

def hellow(a):
    print("HEllowWORLTZ")
    print(a)
    return a

#ANALITIKA
def get_report(analytics, start_date, end_date, view_id, metrics, dimensions):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {'viewId': '129196190', "pageSize": "1000000000",
                 'dateRanges': [{'startDate': start_date, 'endDate': end_date}], 'metrics': metrics,
                 'dimensions': dimensions}]
        },
    ).execute()

def return_ga_data(start_date, end_date, view_id, metrics, dimensions,service):
    return print_response(get_report(service, start_date, end_date, view_id, metrics, dimensions))


def print_response(response):
    list = []
    # get report data
    for report in response.get('reports', []):
        # set column headers
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        for row in rows:
            # create dict for each row
            dict = {}
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            # fill dict with dimension header (key) and dimension value (value)
            for header, dimension in zip(dimensionHeaders, dimensions):
                dict[header] = dimension

            # fill dict with metric header (key) and metric value (value)
            for i, values in enumerate(dateRangeValues):
                for metric, value in zip(metricHeaders, values.get('values')):
                    # set int as int, float a float
                    if ',' in value or '.' in value:
                        dict[metric.get('name')] = float(value)
                    else:
                        dict[metric.get('name')] = int(value)
            list.append(dict)
    df = pd.DataFrame(list)
    return df
#ENDANALITICA
def uelgenerator(string):
    result = re.search(r'/{1}[^/].+', string)
    utm = result.group(0)
    indexslesh = []
    for i in range(len(utm)):
        if utm[i] == '/':
            indexslesh.append(i)
    utmforanalytics = utm[indexslesh[1]:len(utm)]
    return utmforanalytics



#RERURNTALIZAFROMANALITICA
def googlesheets(slovartraf,completeurl):
    df=connect(completeurl)
    df['new_col'] = df['utm_source'] + ' / ' + df['utm_medium']
    a = df.dropna(subset=[list(df)[0]])
    newdf = a[['utm_source', 'utm_medium', 'utm_campaign', 'new_col']]
    slovaritog = {'Уникальная': [0, 0], 'Дайджест': [0, 0], 'SMM репостов': [0, 0],
                  'Инфопартнеры': [0, 0], 'Рассылка из юнисендера': [0, 0], 'Промо в вузах': [0, 0], 'Телеграм': [0, 0],
                  'Таргетинг': [0, 0],
                  'Веб-страница и слайдер': [0, 0], 'Контекстная реклама': [0, 0], 'Органика и неопознанный трафик': [0, 0]}
    for i in list(newdf['new_col']):
        ii = str(i)
        if 'generalbase' in ii or 'mailchimp' in ii:
            slovaritog['Уникальная'][1] += 1
        elif 'digest' in ii or 'Digest' in ii:
            slovaritog['Дайджест'][1] += 1
        elif 'vk-wall' in ii or 'vk_wall' in ii:
            slovaritog['SMM репостов'][1] += 1
        elif 'ip-' in ii or 'ip_' in ii:
            slovaritog['Инфопартнеры'][1] += 1
        elif 'mail' in ii or 'email' in ii or 'Unisender' in ii or 'unisender' in ii or 'utm_source' in ii or 'UniSender' in ii:
            slovaritog['Рассылка из юнисендера'][1] += 1
        elif 'vuz-' in ii or 'vuz_' in ii:
            slovaritog['Промо в вузах'][1] += 1
        elif 'tg /' in ii or 'Tg /' in ii:
            slovaritog['Телеграм'][1] += 1
        elif 'vk / target' in ii or 'vk / targetpost' in ii or 'vk / target-story' in ii or 'insta / target' in ii or 'insta / targetpost' in ii or 'insta / target-story' in ii or 'fb / target' in ii or 'fb / targetpost' in ii:
            slovaritog['Таргетинг'][1] += 1
        elif 'cl-site' in ii or 'Сl-site' in ii or 'cl_site' in ii or 'Сl_site' in ii:
            slovaritog['Веб-страница и слайдер'][1] += 1
        elif 'google / cpc' in ii or 'youtube / instream' in ii or 'yandex / cpc' in ii:
            slovaritog['Контекстная реклама'][1] += 1
        else:
            slovaritog['Органика и неопознанный трафик'][1] += 1

    for i in slovartraf:
        if 'email / generalbase' in i or 'mailchimp' in i:
            slovaritog['Уникальная'][0] += slovartraf[i]
        elif 'digest' in i or 'Digest' in i:
            slovaritog['Дайджест'][0] += slovartraf[i]
        elif 'vk-wall' in i or 'vk_wall' in i:
            slovaritog['SMM репостов'][0] += slovartraf[i]
        elif 'ip-' in i or 'ip_' in i:
            slovaritog['Инфопартнеры'][0] += slovartraf[i]
        elif 'mail' in i or 'email' in i or 'Unisender' in i or 'unisender' in i or 'utm_source' in i or 'UniSender' in i:
            slovaritog['Рассылка из юнисендера'][0] += slovartraf[i]
        elif 'vuz-' in i or 'vuz_' in i:
            slovaritog['Промо в вузах'][0] += slovartraf[i]
        elif 'tg /' in i or 'Tg /' in i:
            slovaritog['Телеграм'][0] += slovartraf[i]
        elif 'vk / target' in i or 'vk / targetpost' in i or 'vk / target-story' in i or 'insta / target' in i or 'insta / targetpost' in i or 'insta / target-story' in i or 'fb / target' in i or 'fb / targetpost' in i:
            slovaritog['Таргетинг'][0] += slovartraf[i]
        elif 'cl-site' in i or 'Сl-site' in i or 'cl_site' in i or 'Сl_site' in i:
            slovaritog['Веб-страница и слайдер'][0] += slovartraf[i]
        elif 'google / cpc' in i or 'youtube / instream' in i or 'yandex / cpc' in i:
            slovaritog['Контекстная реклама'][0] += slovartraf[i]
        else:
            slovaritog['Органика и неопознанный трафик'][0] += slovartraf[i]
    print("Sheets")
    return slovaritog


def googleapi(slovartraf,df,successurl):
    data_names = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == successurl][['ga:sourceMedium']].values))
    data_values = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == successurl][['ga:uniquePageviews']].values))
    slovar = dict(zip(data_names, data_values))
    slovaritog = {'Уникальная': [0, 0], 'Дайджест': [0, 0], 'SMM репостов': [0, 0],
                  'Инфопартнеры': [0, 0], 'Рассылка из юнисендера': [0, 0], 'Промо в вузах': [0, 0], 'Телеграм': [0, 0],
                  'Таргетинг': [0, 0],
                  'Веб-страница и слайдер': [0, 0], 'Контекстная реклама': [0, 0], 'Органика и неопознанный трафик': [0, 0]}
    for i in slovar:
        if 'generalbase' in i or 'mailchimp' in i:
            slovaritog['Уникальная'][1] += slovar[i]
        elif 'digest' in i or 'Digest' in i:
            slovaritog['Дайджест'][1] += slovar[i]
        elif 'vk-wall' in i or 'vk_wall' in i:
            slovaritog['SMM репостов'][1] += slovar[i]
        elif 'ip-' in i or 'ip_' in i:
            slovaritog['Инфопартнеры'][1] += slovar[i]
        elif 'mail' in i or 'email' in i or 'Unisender' in i or 'unisender' in i or 'utm_source' in i or 'UniSender' in i:
            slovaritog['Рассылка из юнисендера'][1] += slovar[i]
        elif 'vuz-' in i or 'vuz_' in i:
            slovaritog['Промо в вузах'][1] += slovar[i]
        elif 'tg /' in i or 'Tg /' in i:
            slovaritog['Телеграм'][1] += slovar[i]
        elif 'vk / target' in i or 'vk / targetpost' in i or 'vk / target-story' in i or 'insta / target' in i or 'insta / targetpost' in i or 'insta / target-story' in i or 'fb / target' in i or 'fb / targetpost' in i:
            slovaritog['Таргетинг'][1] += slovar[i]
        elif 'cl-site' in i or 'Сl-site' in i or 'cl_site' in i or 'Сl_site' in i:
            slovaritog['Веб-страница и слайдер'][1] += slovar[i]
        elif 'google / cpc' in i or 'youtube / instream' in i or 'yandex / cpc' in i:
            slovaritog['Контекстная реклама'][1] += slovar[i]
        else:
            slovaritog['Органика и неопознанный трафик'][1] += slovar[i]

    for i in slovartraf:
        if 'email / generalbase' in i or 'mailchimp' in i:
            slovaritog['Уникальная'][0] += slovartraf[i]
        elif 'digest' in i or 'Digest' in i:
            slovaritog['Дайджест'][0] += slovartraf[i]
        elif 'vk-wall' in i or 'vk_wall' in i:
            slovaritog['SMM репостов'][0] += slovartraf[i]
        elif 'ip-' in i or 'ip_' in i:
            slovaritog['Инфопартнеры'][0] += slovartraf[i]
        elif 'mail' in i or 'email' in i or 'Unisender' in i or 'unisender' in i or 'utm_source' in i or 'UniSender' in i:
            slovaritog['Рассылка из юнисендера'][0] += slovartraf[i]
        elif 'vuz-' in i or 'vuz_' in i:
            slovaritog['Промо в вузах'][0] += slovartraf[i]
        elif 'tg /' in i or 'Tg /' in i:
            slovaritog['Телеграм'][0] += slovartraf[i]
        elif 'vk / target' in i or 'vk / targetpost' in i or 'vk / target-story' in i or 'insta / target' in i or 'insta / targetpost' in i or 'insta / target-story' in i or 'fb / target' in i or 'fb / targetpost' in i:
            slovaritog['Таргетинг'][0] += slovartraf[i]
        elif 'cl-site' in i or 'Сl-site' in i or 'cl_site' in i or 'Сl_site' in i:
            slovaritog['Веб-страница и слайдер'][0] += slovartraf[i]
        elif 'google / cpc' in i or 'youtube / instream' in i or 'yandex / cpc' in i:
            slovaritog['Контекстная реклама'][0] += slovartraf[i]
        else:
            slovaritog['Органика и неопознанный трафик'][0] += slovartraf[i]
    print("API")
    return slovaritog
#ENDRETURNTABLIZAFROMANALITICA





def colvodneyforday(start,stop,urlland):
    credentials = GoogleCredentials(access_token, client_id, client_secret, refresh_token, 3920,
                                    'https://accounts.google.com/o/oauth2/token', 'test')

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('analytics', 'v4', http=http, cache_discovery=False,
                    discoveryServiceUrl='https://analyticsreporting.googleapis.com/$discovery/rest?version=v4')
    urltoLanding=uelgenerator(urlland)
    datedelta = []
    d1 = date(int(start[:4]), int(start[5:7]), int(start[8:10]))
    d2 = date(int(stop[:4]), int(stop[5:7]), int(stop[8:10]))

    # this will give you a list containing all of the dates
    dd = [d1 + timedelta(days=x) for x in range((d2 - d1).days + 1)]
    for x in dd:
        datedelta.append(str(x))
    df = return_ga_data(
        start_date=start,
        end_date=stop,
        view_id='129196190',
        metrics=[{"expression": "ga:uniquePageviews"}, ],
        dimensions=[{'name': 'ga:pagePath'}, {'name': 'ga:sourceMedium'}, {'name': 'ga:date'}],
        service=service,
    )

    data_namestraf = list(itertools.chain.from_iterable(df[df['ga:pagePath'] == urltoLanding].values))
    kolvodneyWEB = 0
    qqq = []
    # print(data_namestraf)
    for j in datedelta:
        datee = []
        for i in range(len(data_namestraf)):
            if data_namestraf[i] == j[:4] + j[5:7] + j[8:10]:
                datee.append(data_namestraf[i:i + 4])
        qqq.append(datee)
    kolvodneyWEB = 0
    kolvodneyKONTEKST = 0
    kolvodnetTARGETING = 0
    k = []
    for i in range(len(qqq)):
        k.append(list(itertools.chain.from_iterable(qqq[i])))
    for i in range(len(k)):
        for j in range(len(k[i])):
            if 'cl-site' in str(k[i][j]) or 'Сl-site' in str(k[i][j]) or 'cl_site' in str(k[i][j]) or 'Сl_site' in str(
                    k[i][j]):
                kolvodneyWEB += 1
                break
            else:
                pass
    for i in range(len(k)):
        for j in range(len(k[i])):
            if 'google / cpc' in str(k[i][j]) or 'youtube / instream' in str(k[i][j]) or 'yandex / cpc' in str(k[i][j]):
                kolvodneyKONTEKST += 1
                break
            else:
                pass
    for i in range(len(k)):
        for j in range(len(k[i])):
            if 'vk / target' in str(k[i][j]) or 'vk / targetpost' in str(k[i][j]) or 'vk / target-story' in str(
                    k[i][j]) or 'insta / target' in str(k[i][j]) or 'insta / targetpost' in str(
                    k[i][j]) or 'insta / target-story' in str(k[i][j]) or 'fb / target' in str(
                    k[i][j]) or 'fb / targetpost' in str(k[i][j]):
                kolvodnetTARGETING += 1
                break
            else:
                pass
    #PICS
    unikalkarry = []
    digestarray = []
    telegaarray = []
    # lif 'digest' in i or 'Digest' in i:
    #  elif 'tg /' in i or 'Tg /' in i:
    for i in range(len(k)):
        for j in range(len(k[i])):
            if 'generalbase' in str(k[i][j]) or 'mailchimp' in str(k[i][j]):
                unikalkarry.append(int(k[i][j - 2]))
            elif 'digest' in str(k[i][j]) or 'Digest' in str(k[i][j]):
                digestarray.append(int(k[i][j - 2]))
            elif 'tg /' in str(k[i][j]) or 'Tg /' in str(k[i][j]):
                telegaarray.append(int(k[i][j - 2]))
            else:
                pass
    #  if 'generalbase' in ii or 'mailchimp' in ii:

    max_value = 0
    for n in unikalkarry:
        if n > max_value:
            max_value = n
    if max_value == 1:
        lenUNIKALKA = sg.find_peaks_cwt(unikalkarry, np.arange(1, max_value + 1),
                                        max_distances=np.arange(1, max_value + 1))
    elif max_value == 0:
        lenUNIKALKA = []
    else:
        lenUNIKALKA = sg.find_peaks_cwt(unikalkarry, np.arange(1, max_value),
                                        max_distances=np.arange(1, max_value))

    max_value = 0
    for n in digestarray:
        if n > max_value:
            max_value = n
    if max_value == 1:
        lenDIGEST = sg.find_peaks_cwt(digestarray, np.arange(1, max_value + 1),
                                      max_distances=np.arange(1, max_value + 1))
    elif max_value == 0:
        lenDIGEST = []
    else:
        lenDIGEST = sg.find_peaks_cwt(digestarray, np.arange(1, max_value),
                                      max_distances=np.arange(1,max_value))


    max_value = 0
    for n in telegaarray:
        if n > max_value:
            max_value = n
    if max_value == 1:
        lenTELEGA = sg.find_peaks_cwt(telegaarray, np.arange(1, max_value + 1),
                                      max_distances=np.arange(1, max_value + 1))
    elif max_value == 0:
        lenTELEGA = []
    else:
        lenTELEGA = sg.find_peaks_cwt(telegaarray, np.arange(1, max_value),
                                      max_distances=np.arange(1, max_value))

    return [kolvodnetTARGETING,kolvodneyWEB,kolvodneyKONTEKST,len(lenUNIKALKA), len(lenDIGEST), len(lenTELEGA)]




def analitica(land,success,start,end,complete):


    credentials = GoogleCredentials(access_token, client_id, client_secret, refresh_token, 3920,
                                    'https://accounts.google.com/o/oauth2/token', 'test')

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('analytics', 'v4', http=http, cache_discovery=False,
                    discoveryServiceUrl='https://analyticsreporting.googleapis.com/$discovery/rest?version=v4')
    #POMENYAT
    start = start
    stop = end
    if datetime.date(int(stop[:4]), int(stop[5:7]), int(stop[8:10]))>datetime.datetime.now().date():
        stop=str(datetime.datetime.now().date())
    else:
        pass
    print('!!!!!!')
    print(stop)
    df = return_ga_data(
        start_date=start,
        end_date=stop,
        view_id='129196190',
        metrics=[{"expression": "ga:uniquePageviews"}, ],
        dimensions=[{'name': 'ga:pagePath'}, {'name': 'ga:sourceMedium'}, ],
        service=service,
    )
    #POMENYAT
    urltoLanding=uelgenerator(land)
    urltoSuccess = uelgenerator(success)
    data_namestraf = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == urltoLanding][['ga:sourceMedium']].values))
    data_valuestraf = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == urltoLanding][['ga:uniquePageviews']].values))
    print(data_namestraf)
    slovartraf = dict(zip(data_namestraf, data_valuestraf))
    try:
        # POMENYAT
        data = googlesheets(slovartraf,complete)
        print('1')
    except:
        data = googleapi(slovartraf,df,urltoSuccess)
        print('2')
    data_names = list(data.keys())
    data_values = list(data.values())

    d = {'Источник': data_names, 'Количество': ['0' for x in data_values],'Сила': ['—' for x in data_values], 'Трафикфакт': [x[0] for x in data_values],
         'Конверсия': [str(int(x[1] / x[0] * 100)) + '%' if x[0] > 0 else x[0] for x in data_values],
         'Регистрациифакт': [x[1] for x in data_values], 'Бюджетплан': ['—' for x in data_values],
         'Бюджетфакт': ['—' for x in data_values]}
    vuz = 0
    set_data_valuestraf = set(data_namestraf)
    for i in set_data_valuestraf:
        if 'vuz-' in i or 'vuz_' in i:
            vuz += 1
    d['Количество'][5] = vuz
    '''colvodneylist = colvodneyforday(start, stop, service, urltoLanding)
    d['Количество'][7] = colvodneylist[0]
    d['Количество'][8] = colvodneylist[1]
    d['Количество'][9] = colvodneylist[2]
    kolvopics = kolvopicsfunct(colvodneylist[3])
    d['Количество'][0] = kolvopics[0]
    d['Количество'][1] = kolvopics[1]
    d['Количество'][6] = kolvopics[2]'''


    panda=pd.DataFrame(data=d)
    pd.set_option('display.max_columns', 700)
    #print(panda)
    return d




if __name__ == "__main__":
    # execute only if run as a script
    print(analitica([{'land': ['https://1.changellenge.com/supply-chain'], 'success': ['https://1.changellenge.com/supply-chain-success'], 'start': ['2019-08-30'], 'end': ['2019-10-30'], 'complete': ['complete'], 'heshteg': ['hash']}]))
