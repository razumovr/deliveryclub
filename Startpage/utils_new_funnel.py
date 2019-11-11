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


from sys import platform


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



def googleapi(slovartraf,df,successurl):
    data_names = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == successurl][['ga:sourceMedium']].values))
    data_values = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == successurl][['ga:uniquePageviews']].values))
    data_compain = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == successurl][['ga:campaign']].values))
    data_term = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == successurl][['ga:keyword']].values))
    data_content = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == successurl][['ga:adContent']].values))
    slovar = dict(zip([data_names[i]+' / '+ data_compain[i]+' / '+ data_term[i]+' / '+ data_content[i] for i in range(len(data_names))], data_values))
    slovaritog ={'Уникальный пакет промо': [0, 0],
                 'Уникальная рассылка': [0, 0],
                 'Digest рассылка по всей базе': [0, 0],
                  'Рассылка по сборному сегементу через mailchimp (например, те кто кликал на стажировки)': [0, 0],
                  'Рассылка по сборной базе под конкретный проект (например, ИТшники из Уфы, 3-4 курс) или Рассылка по базе партнера чемпионата ': [0, 0],
                  'рассылка по базе кейсеров': [0, 0],
                 'рассылка по IT базе': [0, 0],
                  'рассылка по базе инженеров': [0, 0],
                  'рассылка по базе нефтяников': [0, 0],
                 'рассылка по базе бизнес': [0, 0],
                 'рассылка по базе partials': [0, 0],
                  'Рассылка по новой базе hh': [0, 0],
                  'Рассылка по базе курса первокурсника': [0, 0],
                 'Рассылка по старой базе hh': [0, 0],
                  'Рассылка по базе финансистов и экономистов': [0, 0],
                 'Рассылка по базе менеджмента': [0, 0],
                  'Рассылка по базе аналитиков': [0, 0],
                 'рассылка по базе региона Спб': [0, 0],
                  'рассылка по базе региона Сибирь': [0, 0],
                 'рассылка по базе региона Урал': [0, 0],
                  'рассылка по базе региона Волга': [0, 0],
                 'рассылка по базе региона Дальний Восток': [0, 0],
                  'рассылка по базе Казахстана': [0, 0],
                 'рассылка по прошлогодней базе проекта': [0, 0],
                  'рассылка по прошлогодней базе Аламни': [0, 0],
                 'рассылка по прошлогодней базе Школы': [0, 0],
                  'рассылка по прошлогодней базе Тулкита': [0, 0],
                 'рассылка по прошлогодней базе стажировок': [0, 0],
                  'рассылка по базе б2б партнеров (холодные)': [0, 0],
                 'рассылка по базе б2б партнеров (теплые)': [0, 0],
                  'таргетинг тизеры vk': [0, 0],
                 'таргетинг в новостой ленте vk': [0, 0],
                  'таргетинг в VK Stories': [0, 0],
                 'таргетинг в новостой ленте instagram': [0, 0],
                  'таргетинг в Instagram Stories': [0, 0],
                 'таргетинг stories fb': [0, 0],
                  'таргетинг в новостой ленте fb': [0, 0],
                 'таргетинг на лидформу fb':[0,0],
                 'таргетинг на лидформу вк': [0, 0],
                 'SMM:стена вк основная группа': [0, 0],
                  'SMM:стена вк группа Спб': [0, 0],
                 'SMM:стена вк группа Сибири': [0, 0],
                  'SMM:стена вк группа Урала': [0, 0],
                 'SMM:стена вк группа Волги': [0, 0],
                  'SMM:стена вк группа Казахстана': [0, 0],
                 'SMM:рассылка-дайжест ВК в ЛС': [0, 0],
                  'SMM:рассылка о кейс-чемприонатах ВК в ЛС': [0, 0],
                 'SMM:рассылка с вакансиями ВК в ЛС': [0, 0],
                  'SMM:рассылка о мероприятиях ВК в ЛС': [0, 0],
                 'SMM:рассылка со статьями/полезными материалами ВК в ЛС': [0, 0],
                  'SMM:стена клиентской группы ВК': [0, 0],
                 'пост в телеграм-канале': [0, 0],
                  'дайджест в телеграм-канале': [0, 0],
                 'ссылка на главном слайдере': [0, 0],
                  'ссылка на главной в разделе мероприятий': [0, 0],
                 'ссылка на главной в разделе обучения/курсов': [0, 0],
                  'ссылка на главной в разделе чемпионатов': [0, 0],
                 'пуш-уведомление на сайте': [0, 0],
                  'ссылка на странице мероприятий': [0, 0],
                 'ссылка на странице обучение': [0, 0],
                  'ссылка на странице чемпионатов': [0, 0],
                 'ссылка на странице вакансии': [0, 0],
                  'поп-ап на сайте веб-версия': [0, 0],
                 'поп-ап на сайте мобильная версия': [0, 0],
                 'ссылка с личного кабинета':[0,0],
                  'Ссылка по роликом на Yotube-канал': [0, 0],
                 'группа ФБ': [0, 0],
                 'Страница АА в ФБ': [0, 0],
                  'Страница в Твиттере': [0, 0],
                 'ссылка в БИО': [0, 0],
                  'ссылка в сториз': [0, 0],
                 'инфопартнеры:баннер на сайте': [0, 0],
                  'инфопартнеры:пост вконтакте': [0, 0],
                 'инфопартнеры:пост в Telegram': [0, 0],
                 'инфопартнеры:имейл рассылка': [0, 0],
                 'инфопартнеры:статья или анонс на сайте': [0, 0],
                  'инфопартнеры:пост в Twitter': [0, 0],
                 'инфопартнеры:пост в Instagram': [0, 0],
                  'инфопартнеры:пост в Facebook': [0, 0],
                 'Амбассадор договаривается о размещении на онлайн-ресурсах': [0, 0],
                  'Амбассадор собирает офлайн-регистрации': [0, 0],
                 'Размещение в ЦРК': [0, 0],
                  'Размещение в студсовете': [0, 0],
                 'Размещение в профкоме': [0, 0],
                  'Размещение в кейс-клубе': [0, 0],
                 'Размещение в медиа': [0, 0],
                  'Размещение в главной группе вуза': [0, 0],
                 'Размещение для выпускников': [0, 0],
                  'Размещение в бизнес-клубе': [0, 0],
                 'Размещение на кафедре': [0, 0],
                  'Размещение через преподавателей': [0, 0],
                 'Размещение в студенческом научном обществе': [0, 0],
                  'Размещение через онлайн-аутсорс': [0, 0],
                 'Размещение через офлайн-аутсорс': [0, 0],
                  'Роадшоу с флаерами/плакатами (регистрации по QR-коду)': [0, 0],
                 'Роадшоу с анкетами (с дальнейшей оцифровкой)': [0, 0],
                  'Размещение в СМИ': [0, 0],
                 'прозвон по базе hh с отправкой рассылки': [0, 0],
                  'Прозвон по partials с отправкой рассылки': [0, 0],
                 'Прозвон по базам прошлых лет с отправкой рассылки': [0, 0],
                  'Прозвон по каким-либо базам с отправкой рассылки': [0, 0],
                 'Прозвон с регистрацией на звонке': [0, 0],
                  'Яндекс на поиске по брендовым запросам': [0, 0],
                 'Яндекс РСЯ по брендовым запросам': [0, 0],
                  'Яндекс на Поиске по запросам без упоминания бренда': [0, 0],
                 'Яндекс РСЯ по запросам без упоминания бренда': [0, 0],
                  'Google на поиске по брендовым запросам': [0, 0],
                 'Google КМС по брендовым запросам': [0, 0],
                  'Google на Поиске по запросам без упоминания бренда': [0, 0],
                 'Google КМС по запросам без упоминания бренда': [0, 0],
                 'Youtube контекст': [0, 0],
                 'Виртуальный рекрутер': [0, 0],
                  'Органика': [0, 0],
                 'Неопознанный трафик': [0, 0]}
    for i in slovar:
        if 'all / changellenge / unical-promo' in i:
            slovaritog['Уникальный пакет промо'][1] += slovar[i]
        elif 'email / generalbase' in i:
            slovaritog['Уникальная рассылка'][1] += slovar[i]
        elif 'email / digest' in i:
            slovaritog['Digest рассылка по всей базе'][1] += slovar[i]
        elif 'email / segment-mailchimp' in i:
            slovaritog['Рассылка по сборному сегементу через mailchimp (например, те кто кликал на стажировки)'][1] += slovar[i]
        elif 'email / segment' in i:
            slovaritog['Рассылка по сборной базе под конкретный проект (например, ИТшники из Уфы, 3-4 курс)'][1] += slovar[i]
        elif 'email / segment / cup' in i:
            slovaritog['рассылка по базе кейсеров'][1] += slovar[i]
        elif 'email / segment / it' in i:
            slovaritog['рассылка по IT базе'][1] += slovar[i]
        elif 'email / segment / engineers' in i:
            slovaritog['рассылка по базе инженеров'][1] += slovar[i]
        elif 'email / segment / oil' in i:
            slovaritog['рассылка по базе нефтяников'][1] += slovar[i]
        elif 'email / segment / business' in i:
            slovaritog['рассылка по базе бизнес'][1] += slovar[i]
        elif 'email / segment / partials' in i:
            slovaritog['рассылка по базе partials'][1] += slovar[i]
        elif 'email / segment / external' in i:
            slovaritog['Рассылка по новой базе hh'][1] += slovar[i]




        elif 'email / segment / kp' in i:
            slovaritog['Рассылка по базе курса первокурсника'][1] += slovar[i]
        elif 'email / segment / old-external' in i:
            slovaritog['Рассылка по старой базе hh'][1] += slovar[i]
        elif 'email / segment / fin' in i:
            slovaritog['Рассылка по базе финансистов и экономистов'][1] += slovar[i]
        elif 'email / segment / manager' in i:
            slovaritog['Рассылка по базе менеджмента'][1] += slovar[i]
        elif 'email / segment / analytic' in i:
            slovaritog['Рассылка по базе аналитиков'][1] += slovar[i]
        elif 'email / segment / spb' in i:
            slovaritog['рассылка по базе региона Спб'][1] += slovar[i]
        elif 'email / segment / siberia' in i:
            slovaritog['рассылка по базе региона Сибирь'][1] += slovar[i]
        elif 'eemail / segment / ural' in i:
            slovaritog['рассылка по базе региона Урал'][1] += slovar[i]
        elif 'email / segment / volga' in i:
            slovaritog['рассылка по базе региона Волга'][1] += slovar[i]
        elif 'email / segment / dv' in i:
            slovaritog['рассылка по базе региона Дальний Восток'][1] += slovar[i]
        elif 'email / segment / kz' in i:
            slovaritog['рассылка по базе Казахстана'][1] += slovar[i]
        elif 'email / segment / last-year' in i:
            slovaritog['рассылка по прошлогодней базе проекта'][1] += slovar[i]
        elif 'email / segment / alumni' in i:
            slovaritog['рассылка по прошлогодней базе Аламни'][1] += slovar[i]
        elif 'email / segment / school' in i:
            slovaritog['рассылка по прошлогодней базе Школы'][1] += slovar[i]
        elif 'email / segment / toolkit' in i:
            slovaritog['рассылка по прошлогодней базе Тулкита'][1] += slovar[i]
        elif 'email / segment / internship' in i:
            slovaritog['рассылка по прошлогодней базе стажировок'][1] += slovar[i]
        elif 'email / hr-digest / cold' in i:
            slovaritog['рассылка по базе б2б партнеров (холодные)'][1] += slovar[i]
        elif 'email / hr-digest / warm' in i:
            slovaritog['рассылка по базе б2б партнеров (теплые)'][1] += slovar[i]
        elif 'target / vk / tizer' in i:
            slovaritog['таргетинг тизеры vk'][1] += slovar[i]
        elif 'target / vk / post' in i:
            slovaritog['таргетинг в новостой ленте vk'][1] += slovar[i]
        elif 'target / vk / story' in i:
            slovaritog['таргетинг в VK Stories'][1] += slovar[i]
        elif 'target / insta / post' in i:
            slovaritog['таргетинг в новостой ленте instagramа'][1] += slovar[i]
        elif 'target / insta / story' in i:
            slovaritog['таргетинг в Instagram Stories'][1] += slovar[i]
        elif 'target / fb / story' in i:
            slovaritog['таргетинг stories fb'][1] += slovar[i]
        elif 'target / fb / post' in i:
            slovaritog['таргетинг в новостой ленте fb'][1] += slovar[i]
        elif 'target / fb / leadform' in i:
            slovaritog['таргетинг на лидформу fb'][1] += slovar[i]
        elif 'target / vk / leadform' in i:
            slovaritog['таргетинг на лидформу вк'][1] += slovar[i]
        elif 'vk / global / post' in i:
            slovaritog['SMM:стена вк основная группа'][1] += slovar[i]
        elif 'vk / spb / post' in i:
            slovaritog['SMM:стена вк группа Спб'][1] += slovar[i]
        elif 'vk / siberia / post' in i:
            slovaritog['SMM:стена вк группа Сибири'][1] += slovar[i]
        elif 'vk / ural / post' in i:
            slovaritog['SMM:стена вк группа Урала'][1] += slovar[i]
        elif 'vk / volga / post' in i:
            slovaritog['SMM:стена вк группа Волги'][1] += slovar[i]
        elif 'vk / kz / post' in i:
            slovaritog['SMM:стена вк группа Казахстана'][1] += slovar[i]
        elif 'vk / global / digest' in i:
            slovaritog['SMM:рассылка-дайжест ВК в ЛС'][1] += slovar[i]
        elif 'vk / global / cups' in i:
            slovaritog['SMM:рассылка о кейс-чемприонатах ВК в ЛС'][1] += slovar[i]
        elif 'vk / global / vacancy' in i:
            slovaritog['SMM:рассылка с вакансиями ВК в ЛС'][1] += slovar[i]
        elif 'vk / global / events' in i:
            slovaritog['SMM:рассылка о мероприятиях ВК в ЛС'][1] += slovar[i]
        elif 'vk / global / article' in i:
            slovaritog['SMM:рассылка со статьями/полезными материалами ВК в ЛС'][1] += slovar[i]
        elif 'vk / ' in i and 'post / (not set)' in i:
            slovaritog['SMM:стена клиентской группы ВК'][1] += slovar[i]
        elif 'tg / post' in i:
            slovaritog['пост в телеграм-канале'][1] += slovar[i]
        elif 'tg / digest' in i:
            slovaritog['дайджест в телеграм-канале'][1] += slovar[i]
        elif 'cl-site / main / slider' in i:
            slovaritog['ссылка на главном слайдере'][1] += slovar[i]
        elif 'cl-site / main / events' in i:
            slovaritog['ссылка на главной в разделе мероприятий'][1] += slovar[i]
        elif 'cl-site / main / education' in i:
            slovaritog['ссылка на главной в разделе обучения/курсов'][1] += slovar[i]
        elif 'cl-site / main / champs' in i:
            slovaritog['ссылка на главной в разделе чемпионатов'][1] += slovar[i]
        elif 'cl-site / push' in i:
            slovaritog['пуш-уведомление на сайте'][1] += slovar[i]
        elif 'cl-site / page / event' in i:
            slovaritog['ссылка на странице мероприятий'][1] += slovar[i]
        elif 'cl-site / page / education' in i:
            slovaritog['ссылка на странице обучение'][1] += slovar[i]
        elif 'cl-site / page / champs' in i:
            slovaritog['ссылка на странице чемпионатов'][1] += slovar[i]
        elif 'cl-site / page / vacancy' in i:
            slovaritog['ссылка на странице вакансии'][1] += slovar[i]
        elif 'cl-site / popup / desktop' in i:
            slovaritog['поп-ап на сайте веб-версия'][1] += slovar[i]
        elif 'cl-site / popup / mobile' in i:
            slovaritog['поп-ап на сайте мобильная версия'][1] += slovar[i]
        elif 'cl-site / main / personal' in i:
            slovaritog['ссылка с личного кабинета'][1] += slovar[i]
        elif 'youtube / video' in i:
            slovaritog['Ссылка по роликом на Yotube-канал'][1] += slovar[i]
        elif 'fb / post' in i:
            slovaritog['группа ФБ'][1] += slovar[i]
        elif 'fb / post / aa' in i:
            slovaritog['Страница АА в ФБ'][1] += slovar[i]
        elif 'twitter / post / aa' in i:
            slovaritog['Страница в Твиттере'][1] += slovar[i]
        elif 'inst / bio' in i:
            slovaritog['ссылка в БИО'][1] += slovar[i]
        elif 'inst / stories' in i:
            slovaritog['ссылка в сториз'][1] += slovar[i]
        elif 'ip /' in i and 'banner /' in i:
            slovaritog['инфопартнеры:баннер на сайте'][1] += slovar[i]
        elif 'ip /' in i and 'vk-post /' in i:
            slovaritog['инфопартнеры:пост вконтакте'][1] += slovar[i]
        elif 'ip /' in i and 'tg-post /' in i:
            slovaritog['инфопартнеры:пост в Telegram'][1] += slovar[i]
        elif 'ip /' in i and 'email /' in i:
            slovaritog['инфопартнеры:имейл рассылка'][1] += slovar[i]
        elif 'ip /' in i and 'article /' in i:
            slovaritog['инфопартнеры:статья или анонс на сайте'][1] += slovar[i]
        elif 'ip /' in i and 'tw-post /' in i:
            slovaritog['инфопартнеры:пост в Twitter'][1] += slovar[i]
        elif 'ip /' in i and 'inst-post /' in i:
            slovaritog['инфопартнеры:пост в Instagram'][1] += slovar[i]
        elif 'ip /' in i and 'fb-post /' in i:
            slovaritog['инфопартнеры:пост в Facebook'][1] += slovar[i]
        elif 'amb /' in i and 'online /' in i:
            slovaritog['Амбассадор договаривается о размещении на онлайн-ресурсах'][1] += slovar[i]
        elif 'amb /' in i and 'offline /' in i:
            slovaritog['Амбассадор собирает офлайн-регистрации'][1] += slovar[i]
        elif 'vuz /' in i and 'crk / chat /' in i:
            slovaritog['Размещение в ЦРК'][1] += slovar[i]
        elif 'vuz /' in i and 'studsovet / vk-post /' in i:
            slovaritog['Размещение в студсовете'][1] += slovar[i]
        elif 'vuz /' in i and 'profkom / fb-post /' in i:
            slovaritog['Размещение в профкоме'][1] += slovar[i]
        elif 'vuz /' in i and 'kk / website /' in i:
            slovaritog['Размещение в кейс-клубе'][1] += slovar[i]
        elif 'vuz /' in i and 'media / email /' in i:
            slovaritog['Размещение в медиа'][1] += slovar[i]
        elif 'vuz /' in i and 'maingroup / article /' in i:
            slovaritog['Размещение в главной группе вуза'][1] += slovar[i]
        elif 'vuz /' in i and 'alumni / webinar /' in i:
            slovaritog['Размещение для выпускников'][1] += slovar[i]
        elif 'vuz /' in i and 'bk /' in i:
            slovaritog['Размещение в бизнес-клубе'][1] += slovar[i]
        elif 'vuz /' in i and 'kafedra /' in i:
            slovaritog['Размещение на кафедре'][1] += slovar[i]
        elif 'vuz /' in i and 'teacher /' in i:
            slovaritog['Размещение через преподавателей'][1] += slovar[i]
        elif 'vuz /' in i and 'sno /' in i:
            slovaritog['Размещение в студенческом научном обществе'][1] += slovar[i]
        elif 'vuz /' in i and 'online-outsors /' in i:
            slovaritog['Размещение через онлайн-аутсорс'][1] += slovar[i]
        elif 'vuz /' in i and 'offline-outsors /' in i:
            slovaritog['Размещение через офлайн-аутсорс'][1] += slovar[i]
        elif 'vuz /' in i and 'flyer /' in i:
            slovaritog['Роадшоу с флаерами/плакатами (регистрации по QR-коду)'][1] += slovar[i]
        elif 'vuz /' in i and 'roadshow /' in i:
            slovaritog['Роадшоу с анкетами (с дальнейшей оцифровкой)'][1] += slovar[i]
        elif 'smi /' in i and '(not set) / (not set)' in i:
            slovaritog['Размещение в СМИ '][1] += slovar[i]
        elif 'tlm / email / external' in i:
            slovaritog['прозвон по базе hh с отправкой рассылки'][1] += slovar[i]
        elif 'tlm / email / partials' in i:
            slovaritog['Прозвон по partials с отправкой рассылки'][1] += slovar[i]
        elif 'tlm / email / last-year' in i:
            slovaritog['Прозвон по базам прошлых лет с отправкой рассылки'][1] += slovar[i]
        elif 'tlm / email' in i:
            slovaritog['Прозвон по каким-либо базам с отправкой рассылки'][1] += slovar[i]
        elif 'tlm / reg' in i:
            slovaritog['Прозвон с регистрацией на звонке'][1] += slovar[i]
        elif 'yandex / cpc' in i and 'brand' in i:
            slovaritog['Яндекс на поиске по брендовым запросам'][1] += slovar[i]
        elif 'yandex / cpm' in i and 'brand' in i:
            slovaritog['Яндекс РСЯ по брендовым запросам'][1] += slovar[i]
        elif 'yandex / cpc' in i and 'general' in i:
            slovaritog['Яндекс на Поиске по запросам без упоминания бренда'][1] += slovar[i]
        elif 'yandex / cpm' in i and 'general' in i:
            slovaritog['Яндекс РСЯ по запросам без упоминания бренда'][1] += slovar[i]
        elif 'google / cpc' in i and 'brand' in i:
            slovaritog['Google на поиске по брендовым запросам'][1] += slovar[i]
        elif 'google / cpm' in i and 'brand' in i:
            slovaritog['Google КМС по брендовым запросам'][1] += slovar[i]
        elif 'google / cpc' in i and 'general' in i:
            slovaritog['Google на Поиске по запросам без упоминания бренда'][1] += slovar[i]
        elif 'google / cpm' in i and 'general' in i:
            slovaritog['Google КМС по запросам без упоминания бренда'][1] += slovar[i]
        elif 'youtube / cpm' in i and 'brand' in i:
            slovaritog['Youtube контекст'][1] += slovar[i]
        elif 'external-lidgen / cpc / premium' in i:
            slovaritog['Виртуальный рекрутер'][1] += slovar[i]
        elif '(direct) / (none)' in i or 'referral' in i or 'organic' in i:
            slovaritog['Органика'][1] += slovar[i]
        else:
            slovaritog['Неопознанный трафик'][1] += slovar[i]


    for i in slovartraf:
        if 'all / changellenge / unical-promo' in i:
            slovaritog['Уникальный пакет промо'][0] += slovartraf[i]
        elif 'email / generalbase' in i:
            slovaritog['Уникальная рассылка'][0] += slovartraf[i]
        elif 'email / digest' in i:
            slovaritog['Digest рассылка по всей базе'][0] += slovartraf[i]
        elif 'email / segment-mailchimp' in i:
            slovaritog['Рассылка по сборному сегементу через mailchimp (например, те кто кликал на стажировки)'][0] += slovartraf[i]
        elif 'email / segment' in i:
            slovaritog['Рассылка по сборной базе под конкретный проект (например, ИТшники из Уфы, 3-4 курс)'][0] += slovartraf[i]
        elif 'email / segment / cup' in i:
            slovaritog['рассылка по базе кейсеров'][0] += slovartraf[i]
        elif 'email / segment / it' in i:
            slovaritog['рассылка по IT базе'][0] += slovartraf[i]
        elif 'email / segment / engineers' in i:
            slovaritog['рассылка по базе инженеров'][0] += slovartraf[i]
        elif 'email / segment / oil' in i:
            slovaritog['рассылка по базе нефтяников'][0] += slovartraf[i]
        elif 'email / segment / business' in i:
            slovaritog['рассылка по базе бизнес'][0] += slovartraf[i]
        elif 'email / segment / partials' in i:
            slovaritog['рассылка по базе partials'][0] += slovartraf[i]
        elif 'email / segment / external' in i:
            slovaritog['Рассылка по новой базе hh'][0] += slovartraf[i]




        elif 'email / segment / kp' in i:
            slovaritog['Рассылка по базе курса первокурсника'][0] += slovartraf[i]
        elif 'email / segment / old-external' in i:
            slovaritog['Рассылка по старой базе hh'][0] += slovartraf[i]
        elif 'email / segment / fin' in i:
            slovaritog['Рассылка по базе финансистов и экономистов'][0] += slovartraf[i]
        elif 'email / segment / manager' in i:
            slovaritog['Рассылка по базе менеджмента'][0] += slovartraf[i]
        elif 'email / segment / analytic' in i:
            slovaritog['Рассылка по базе аналитиков'][0] += slovartraf[i]
        elif 'email / segment / spb' in i:
            slovaritog['рассылка по базе региона Спб'][0] += slovartraf[i]
        elif 'email / segment / siberia' in i:
            slovaritog['рассылка по базе региона Сибирь'][0] += slovartraf[i]
        elif 'email / segment / ural' in i:
            slovaritog['рассылка по базе региона Урал'][0] += slovartraf[i]
        elif 'email / segment / volga' in i:
            slovaritog['рассылка по базе региона Волга'][0] += slovartraf[i]
        elif 'email / segment / dv' in i:
            slovaritog['рассылка по базе региона Дальний Восток'][0] += slovartraf[i]
        elif 'email / segment / kz' in i:
            slovaritog['рассылка по базе Казахстана'][0] += slovartraf[i]
        elif 'email / segment / last-year' in i:
            slovaritog['рассылка по прошлогодней базе проекта'][0] += slovartraf[i]
        elif 'email / segment / alumni' in i:
            slovaritog['рассылка по прошлогодней базе Аламни'][0] += slovartraf[i]
        elif 'email / segment / school' in i:
            slovaritog['рассылка по прошлогодней базе Школы'][0] += slovartraf[i]
        elif 'email / segment / toolkit' in i:
            slovaritog['рассылка по прошлогодней базе Тулкита'][0] += slovartraf[i]
        elif 'email / segment / internship' in i:
            slovaritog['рассылка по прошлогодней базе стажировок'][0] += slovartraf[i]
        elif 'email / hr-digest / cold' in i:
            slovaritog['рассылка по базе б2б партнеров (холодные)'][0] += slovartraf[i]
        elif 'email / hr-digest / warm' in i:
            slovaritog['рассылка по базе б2б партнеров (теплые)'][0] += slovartraf[i]
        elif 'target / vk / tizer' in i:
            slovaritog['таргетинг тизеры vk'][0] += slovartraf[i]
        elif 'target / vk / post' in i:
            slovaritog['таргетинг в новостой ленте vk'][0] += slovartraf[i]
        elif 'target / vk / story' in i:
            slovaritog['таргетинг в VK Stories'][0] += slovartraf[i]
        elif 'target / insta / post' in i:
            slovaritog['таргетинг в новостой ленте instagramа'][0] += slovartraf[i]
        elif 'target / insta / story' in i:
            slovaritog['таргетинг в Instagram Stories'][0] += slovartraf[i]
        elif 'target / fb / story' in i:
            slovaritog['таргетинг stories fb'][0] += slovartraf[i]
        elif 'target / fb / post' in i:
            slovaritog['таргетинг в новостой ленте fb'][0] += slovartraf[i]
        elif 'target / fb / leadform' in i:
            slovaritog['таргетинг на лидформу fb'][0] += slovartraf[i]
        elif 'target / vk / leadform' in i:
            slovaritog['таргетинг на лидформу вк'][0] += slovartraf[i]
        elif 'vk / global / post' in i:
            slovaritog['SMM:стена вк основная группа'][0] += slovartraf[i]
        elif 'vk / spb / post' in i:
            slovaritog['SMM:стена вк группа Спб'][0] += slovartraf[i]
        elif 'vk / siberia / post' in i:
            slovaritog['SMM:стена вк группа Сибири'][0] += slovartraf[i]
        elif 'vk / ural / post' in i:
            slovaritog['SMM:стена вк группа Урала'][0] += slovartraf[i]
        elif 'vk / volga / post' in i:
            slovaritog['SMM:стена вк группа Волги'][0] += slovartraf[i]
        elif 'vk / kz / post' in i:
            slovaritog['SMM:стена вк группа Казахстана'][0] += slovartraf[i]
        elif 'vk / global / digest' in i:
            slovaritog['SMM:рассылка-дайжест ВК в ЛС'][0] += slovartraf[i]
        elif 'vk / global / cups' in i:
            slovaritog['SMM:рассылка о кейс-чемприонатах ВК в ЛС'][0] += slovartraf[i]
        elif 'vk / global / vacancy' in i:
            slovaritog['SMM:рассылка с вакансиями ВК в ЛС'][0] += slovartraf[i]
        elif 'vk / global / events' in i:
            slovaritog['SMM:рассылка о мероприятиях ВК в ЛС'][0] += slovartraf[i]
        elif 'vk / global / article' in i:
            slovaritog['SMM:рассылка со статьями/полезными материалами ВК в ЛС'][0] += slovartraf[i]
        elif 'vk / ' in i and 'post / (not set)' in i:
            slovaritog['SMM:стена клиентской группы ВК'][0] += slovartraf[i]
        elif 'tg / post' in i:
            slovaritog['пост в телеграм-канале'][0] += slovartraf[i]
        elif 'tg / digest' in i:
            slovaritog['дайджест в телеграм-канале'][0] += slovartraf[i]
        elif 'cl-site / main / slider' in i:
            slovaritog['ссылка на главном слайдере'][0] += slovartraf[i]
        elif 'cl-site / main / events' in i:
            slovaritog['ссылка на главной в разделе мероприятий'][0] += slovartraf[i]
        elif 'cl-site / main / education' in i:
            slovaritog['ссылка на главной в разделе обучения/курсов'][0] += slovartraf[i]
        elif 'cl-site / main / champs' in i:
            slovaritog['ссылка на главной в разделе чемпионатов'][0] += slovartraf[i]
        elif 'cl-site / push' in i:
            slovaritog['пуш-уведомление на сайте'][0] += slovartraf[i]
        elif 'cl-site / page / event' in i:
            slovaritog['ссылка на странице мероприятий'][0] += slovartraf[i]
        elif 'cl-site / page / education' in i:
            slovaritog['ссылка на странице обучение'][0] += slovartraf[i]
        elif 'cl-site / page / champs' in i:
            slovaritog['ссылка на странице чемпионатов'][0] += slovartraf[i]
        elif 'cl-site / page / vacancy' in i:
            slovaritog['ссылка на странице вакансии'][0] += slovartraf[i]
        elif 'cl-site / popup / desktop' in i:
            slovaritog['поп-ап на сайте веб-версия'][0] += slovartraf[i]
        elif 'cl-site / popup / mobile' in i:
            slovaritog['поп-ап на сайте мобильная версия'][0] += slovartraf[i]
        elif 'cl-site / main / personal' in i:
            slovaritog['ссылка с личного кабинета'][0] += slovartraf[i]
        elif 'youtube / video' in i:
            slovaritog['Ссылка по роликом на Yotube-канал'][0] += slovartraf[i]
        elif 'fb / post' in i and '(not set) / (not set)' in i:
            slovaritog['группа ФБ'][0] += slovartraf[i]
        elif 'fb / post / aa' in i:
            slovaritog['Страница АА в ФБ'][0] += slovartraf[i]
        elif 'twitter / post / aa' in i:
            slovaritog['Страница в Твиттере'][0] += slovartraf[i]
        elif 'inst / bio' in i:
            slovaritog['ссылка в БИО'][0] += slovartraf[i]
        elif 'inst / stories' in i:
            slovaritog['ссылка в сториз'][0] += slovartraf[i]
        elif 'ip /' in i and 'banner /' in i:
            slovaritog['инфопартнеры:баннер на сайте'][0] += slovartraf[i]
        elif 'ip /' in i and 'vk-post /' in i:
            slovaritog['инфопартнеры:пост вконтакте'][0] += slovartraf[i]
        elif 'ip /' in i and 'tg-post /' in i:
            slovaritog['инфопартнеры:пост в Telegram'][0] += slovartraf[i]
        elif 'ip /' in i and 'email /' in i:
            slovaritog['инфопартнеры:имейл рассылка'][0] += slovartraf[i]
        elif 'ip /' in i and 'article /' in i:
            slovaritog['инфопартнеры:статья или анонс на сайте'][0] += slovartraf[i]
        elif 'ip /' in i and 'tw-post /' in i:
            slovaritog['инфопартнеры:пост в Twitter'][0] += slovartraf[i]
        elif 'ip /' in i and 'inst-post /' in i:
            slovaritog['инфопартнеры:пост в Instagram'][0] += slovartraf[i]
        elif 'ip /' in i and 'fb-post /' in i:
            slovaritog['инфопартнеры:пост в Facebook'][0] += slovartraf[i]
        elif 'amb /' in i and 'online /' in i:
            slovaritog['Амбассадор договаривается о размещении на онлайн-ресурсах'][0] += slovartraf[i]
        elif 'amb /' in i and 'offline /' in i:
            slovaritog['Амбассадор собирает офлайн-регистрации'][0] += slovartraf[i]
        elif 'vuz /' in i and 'crk / chat /' in i:
            slovaritog['Размещение в ЦРК'][0] += slovartraf[i]
        elif 'vuz /' in i and 'studsovet / vk-post /' in i:
            slovaritog['Размещение в студсовете'][0] += slovartraf[i]
        elif 'vuz /' in i and 'profkom / fb-post /' in i:
            slovaritog['Размещение в профкоме'][0] += slovartraf[i]
        elif 'vuz /' in i and 'kk / website /' in i:
            slovaritog['Размещение в кейс-клубе'][0] += slovartraf[i]
        elif 'vuz /' in i and 'media / email /' in i:
            slovaritog['Размещение в медиа'][0] += slovartraf[i]
        elif 'vuz /' in i and 'maingroup / article /' in i:
            slovaritog['Размещение в главной группе вуза'][0] += slovartraf[i]
        elif 'vuz /' in i and 'alumni / webinar /' in i:
            slovaritog['Размещение для выпускников'][0] += slovartraf[i]
        elif 'vuz /' in i and 'bk /' in i:
            slovaritog['Размещение в бизнес-клубе'][0] += slovartraf[i]
        elif 'vuz /' in i and 'kafedra /' in i:
            slovaritog['Размещение на кафедре'][0] += slovartraf[i]
        elif 'vuz /' in i and 'teacher /' in i:
            slovaritog['Размещение через преподавателей'][0] += slovartraf[i]
        elif 'vuz /' in i and 'sno /' in i:
            slovaritog['Размещение в студенческом научном обществе'][0] += slovartraf[i]
        elif 'vuz /' in i and 'online-outsors /' in i:
            slovaritog['Размещение через онлайн-аутсорс'][0] += slovartraf[i]
        elif 'vuz /' in i and 'offline-outsors /' in i:
            slovaritog['Размещение через офлайн-аутсорс'][0] += slovartraf[i]
        elif 'vuz /' in i and 'flyer /' in i:
            slovaritog['Роадшоу с флаерами/плакатами (регистрации по QR-коду)'][0] += slovartraf[i]
        elif 'vuz /' in i and 'roadshow /' in i:
            slovaritog['Роадшоу с анкетами (с дальнейшей оцифровкой)'][0] += slovartraf[i]
        elif 'smi /' in i and '(not set) / (not set)' in i:
            slovaritog['Размещение в СМИ '][0] += slovartraf[i]
        elif 'tlm / email / external' in i:
            slovaritog['прозвон по базе hh с отправкой рассылки'][0] += slovartraf[i]
        elif 'tlm / email / partials' in i:
            slovaritog['Прозвон по partials с отправкой рассылки'][0] += slovartraf[i]
        elif 'tlm / email / last-year' in i:
            slovaritog['Прозвон по базам прошлых лет с отправкой рассылки'][0] += slovartraf[i]
        elif 'tlm / email' in i:
            slovaritog['Прозвон по каким-либо базам с отправкой рассылки'][0] += slovartraf[i]
        elif 'tlm / reg' in i:
            slovaritog['Прозвон с регистрацией на звонке'][0] += slovartraf[i]
        elif 'yandex / cpc' in i and 'brand' in i:
            slovaritog['Яндекс на поиске по брендовым запросам'][0] += slovartraf[i]
        elif 'yandex / cpm' in i and 'brand' in i:
            slovaritog['Яндекс РСЯ по брендовым запросам'][0] += slovartraf[i]
        elif 'yandex / cpc' in i and 'general' in i:
            slovaritog['Яндекс на Поиске по запросам без упоминания бренда'][0] += slovartraf[i]
        elif 'yandex / cpm' in i and 'general' in i:
            slovaritog['Яндекс РСЯ по запросам без упоминания бренда'][0] += slovartraf[i]
        elif 'google / cpc' in i and 'brand' in i:
            slovaritog['Google на поиске по брендовым запросам'][0] += slovartraf[i]
        elif 'google / cpm' in i and 'brand' in i:
            slovaritog['Google КМС по брендовым запросам'][0] += slovartraf[i]
        elif 'google / cpc' in i and 'general' in i:
            slovaritog['Google на Поиске по запросам без упоминания бренда'][0] += slovartraf[i]
        elif 'google / cpm' in i and 'general' in i:
            slovaritog['Google КМС по запросам без упоминания бренда'][0] += slovartraf[i]
        elif 'youtube / cpm' in i and 'brand' in i:
            slovaritog['Youtube контекст'][0] += slovartraf[i]
        elif 'external-lidgen / cpc / premium' in i:
            slovaritog['Виртуальный рекрутер'][0] += slovartraf[i]
        elif '(direct) / (none)' in i or 'referral' in i or 'organic' in i:
            slovaritog['Органика'][0] += slovartraf[i]
        else:
            slovaritog['Неопознанный трафик'][0] += slovartraf[i]

    print("API")
    return slovaritog
#ENDRETURNTABLIZAFROMANALITICA





def colvodneyforday_new_funnel(start,stop,urlland):
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
        dimensions=[{'name': 'ga:pagePath'}, {'name': 'ga:sourceMedium'},{'name': 'ga:campaign'},{'name': 'ga:keyword'},{'name': 'ga:adContent'}, {'name': 'ga:date'}],
        service=service,
    )


    data_namestraf = list(itertools.chain.from_iterable(df[df['ga:pagePath'] == urltoLanding][['ga:pagePath','ga:sourceMedium','ga:campaign','ga:keyword','ga:adContent','ga:date','ga:uniquePageviews']].values))
    qqq = []
    for j in datedelta:
        datee = []
        for i in range(len(data_namestraf)):
            if data_namestraf[i] == j[:4] + j[5:7] + j[8:10]:
                datee.append(data_namestraf[i:i+7])
        qqq.append(datee)
    for i in range(len(qqq)):
        for k in range(len(qqq[i])):
            if len(qqq[i][k]) == 7:
                myString = ' / '.join(qqq[i][k][-4:])
                qqq[i][k] = [qqq[i][k][0], qqq[i][k][1], myString]
            else:
                pass


    k = []
    for i in range(len(qqq)):
        k.append(list(itertools.chain.from_iterable(qqq[i])))


    anew = list(itertools.chain.from_iterable(k))
    em = {
        'all / changellenge / unical-promo': 0,
        'email / generalbase': 0,
        'email / digest': 0,
        'email / segment-mailchimp': 0,
        'email / segment': 0,
        'email / segment / cup': 0,
        'email / segment / it': 0,
        'email / segment / engineers': 0,
        'email / segment / oil': 0,
        'email / segment / business': 0,
        'email / segment / partials': 0,
        'email / segment / external': 0,
        'email / segment / kp': 0,
        'email / segment / old-external': 0,
        'email / segment / fin': 0,
        'email / segment / manager': 0,
        'email / segment / analytic': 0,
        'email / segment / spb': 0,
        'email / segment / siberia': 0,
        'email / segment / ural': 0,
        'email / segment / volga': 0,
        'email / segment / dv': 0,
        'email / segment / kz': 0,
        'email / segment / last-year': 0,
        'email / segment / alumni': 0,
        'email / segment / school': 0,
        'email / segment / toolkit': 0,
        'email / segment / internship': 0,
        'email / hr-digest / cold': 0,
        'email / hr-digest / warm': 0,
        'vk / global / post': 0,
        'vk / spb / post': 0,
        'vk / siberia / post': 0,
        'vk / ural / post': 0,
        'vk / volga / post': 0,
        'vk / kz / post': 0,
        'vk / global / digest': 0,
        'vk / global / cups': 0,
        'vk / global / vacancy': 0,
        'vk / global / events': 0,
        'vk / global / article': 0,
        'post / (not set)': 0,
        'tg / post': 0,
        'tg / digest': 0,
        'youtube / video': 0,
        'fb / post': 0,
        'fb / post / aa': 0,
        'twitter / post / aa': 0,
        'inst / bio': 0,
        'inst / stories': 0,
        'ip / banner': 0,
        'ip / vk-post': 0,
        'ip / tg-post': 0,
        'ip / email': 0,
        'ip / article': 0,
        'ip / tw-post': 0,
        'ip / inst-post': 0,
        'ip / fb-post': 0,
        'amb / online': 0,
        'amb / offline': 0,
        'vuz / crk': 0,
        'vuz / studsovet': 0,
        'vuz / profkom': 0,
        'vuz / kk': 0,
        'vuz / media': 0,
        'vuz / maingroup': 0,
        'vuz / alumni': 0,
        'vuz / bk': 0,
        'vuz / kafedra': 0,
        'vuz / teacher': 0,
        'vuz / sno': 0,
        'vuz / online-outsors': 0,
        'vuz / offline-outsors': 0,
        'vuz / flyer': 0,
        'vuz / roadshow': 0,
        'smi /': 0,
        'tlm / email / external': 0,
        'tlm / email / partials': 0,
        'tlm / email / last-year': 0,
        'tlm / email': 0,
        'tlm / reg': 0,
        'external-lidgen / cpc / premium': 0,
    }
    for i in em.keys():
        max_value = 0
        mas = []
        for j in range(len(anew)):
            if type(anew[j])==str:
                if i in anew[j]:
                    mas.append(anew[j - 1])
                elif 'ip /' in anew[j] and 'banner /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'ip /' in anew[j] and 'vk-post /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'ip /' in anew[j] and 'tg-post /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'ip /' in anew[j] and 'email /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'ip /' in anew[j] and 'article /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'ip /' in anew[j] and 'tw-post /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'ip /' in anew[j] and 'inst-post /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'ip /' in anew[j] and 'fb-post /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'amb /' in anew[j] and 'online /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'amb /' in anew[j] and 'offline /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'crk / chat /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'studsovet / vk-post /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'profkom / fb-post /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'kk / website /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'media / email /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'maingroup / article /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'alumni / webinar /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'bk /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'kafedra /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'teacher /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'sno /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'online-outsors /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'offline-outsors /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'flyer /' in anew[j]:
                    mas.append(anew[j - 1])
                elif 'vuz /' in anew[j] and 'roadshow /' in anew[j]:
                    mas.append(anew[j - 1])
        for n in mas:
            if n > max_value:
                max_value = n
        if max_value == 1:
            lenUNIKALKA = sg.find_peaks_cwt(mas, np.arange(1, max_value + 1),
                                            max_distances=np.arange(1, max_value + 1))
        elif max_value == 0:
            lenUNIKALKA = []
        else:
            lenUNIKALKA = sg.find_peaks_cwt(mas, np.arange(1, max_value),
                                            max_distances=np.arange(1, max_value))
        em[i] = len(lenUNIKALKA)

    em['target / vk / tizer']=0
    em['target / vk / post']=0
    em['target / vk / story']=0
    em['target / insta / post']=0
    em['target / insta / story']=0
    em['target / fb / story']=0
    em['target / fb / post']=0
    em['target / fb / leadform']=0
    em['target / vk / leadform']=0
    em['cl-site / main / slider']=0
    em['cl-site / main / events']=0
    em['cl-site / main / education']=0
    em['cl-site / main / champs']=0
    em['cl-site / push']=0
    em['cl-site / page / event']=0
    em['cl-site / page / education']=0
    em['cl-site / page / champs']=0
    em['cl-site / page / vacancy']= 0
    em['cl-site / popup / desktop']=0
    em['cl-site / popup / mobile']=0
    em['cl-site / main / personal']=0
    em['yandex / cpc / brand']=0
    em['yandex / cpm / brand']=0
    em['yandex / cpc / general']=0
    em['yandex / cpm / general']=0
    em['google / cpc / brand']=0
    em['google / cpm / brand']=0
    em['google / cpc / general']=0
    em['google / cpm / general']=0
    em['youtube / cpm / general']=0
    em['(direct) / (none)']=0

    for i in anew:
        if type(i)==str:
            if 'target / vk / tizer' in i:
                em['target / vk / tizer'] +=1
            elif 'target / vk / post' in i:
                em['target / vk / post'] +=1
            elif 'target / vk / story' in i:
                em['target / vk / story'] +=1
            elif 'target / fb / story' in i:
                em['target / fb / story'] +=1
            elif 'target / fb / post' in i:
                em['target / fb / post'] +=1
            elif 'target / fb / leadform' in i:
                em['target / fb / leadform'] +=1
            elif 'target / vk / leadform' in i:
                em['target / vk / leadform'] +=1
            elif 'cl-site / main / slider' in i:
                em['cl-site / main / slider'] +=1
            elif 'cl-site / main / events' in i:
                em['cl-site / main / events'] +=1
            elif 'cl-site / main / education' in i:
                em['cl-site / main / education'] +=1
            elif 'cl-site / page / champs' in i:
                em['cl-site / page / champs'] +=1
            elif 'cl-site / page / vacancy' in i:
                em['cl-site / page / vacancy'] +=1
            elif 'tcl-site / popup / desktop' in i:
                em['cl-site / popup / desktop'] +=1
            elif 'cl-site / popup / mobile' in i:
                em['cl-site / popup / mobile'] +=1
            elif 'cl-site / main / personal' in i:
                em['cl-site / main / personal'] +=1
            elif 'yandex / cpc' in i and 'brand' in i:
                em['yandex / cpc / brand'] +=1
            elif 'yandex / cpm' in i and 'brand' in i:
                em['yandex / cpm / brand'] +=1
            elif 'yandex / cpc' in i and 'general' in i:
                em['yandex / cpc / general'] +=1
            elif 'yandex / cpm' in i and 'general' in i:
                em['yandex / cpm / general'] +=1
            elif 'google / cpc' in i and 'brand' in i:
                em['google / cpc / brand'] +=1
            elif 'google / cpm' in i and 'brand' in i:
                em['google / cpm / brand'] +=1
            elif 'google / cpc' in i and 'general' in i:
                em['google / cpc / general'] +=1
            elif 'google / cpm' in i and 'general' in i:
                em['google / cpm / general'] +=1
            elif 'youtube / cpm' in i and 'brand' in i:
                em['youtube / cpm / general'] +=1
            #elif '(direct) / (none)' in i or 'referral' in i or 'organic' in i:
             #   em['(direct) / (none)'] +=1


    '''
    
    kolvodneyWEB = 0
    kolvodneyKONTEKST = 0
    kolvodnetTARGETING = 0
    kolvodneyORGANICA=0
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
    for i in range(len(k)):
        for j in range(len(k[i])):
            if '(direct) / (none)' in str(k[i][j]) or 'referral' in str(k[i][j]) or 'organic' in str(k[i][j]):
                kolvodneyORGANICA += 1
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
                if platform == "darwin":
                    unikalkarry.append(int(k[i][j -2]))
                else:
                    unikalkarry.append(int(k[i][j -2]))
            elif 'digest' in str(k[i][j]) or 'Digest' in str(k[i][j]):
                if platform == "darwin":
                    digestarray.append(int(k[i][j -2]))
                else:
                    digestarray.append(int(k[i][j -2]))
            elif 'tg /' in str(k[i][j]) or 'Tg /' in str(k[i][j]):
                if platform == "darwin":
                    telegaarray.append(int(k[i][j -2]))
                else:
                    telegaarray.append(int(k[i][j -2]))
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

    return [kolvodnetTARGETING,kolvodneyWEB,kolvodneyKONTEKST,kolvodneyORGANICA,len(lenUNIKALKA), len(lenDIGEST), len(lenTELEGA)]'''
    return em




def analitica_new_funnel(land,success,start,end):


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
        dimensions=[{'name': 'ga:pagePath'}, {'name': 'ga:sourceMedium'},{'name': 'ga:campaign'},{'name': 'ga:keyword'},{'name': 'ga:adContent'}],
        service=service,
    )
    #POMENYAT
    urltoLanding=uelgenerator(land)
    urltoSuccess = uelgenerator(success)
    data_namestraf = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == urltoLanding][['ga:sourceMedium']].values))
    data_valuestraf = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == urltoLanding][['ga:uniquePageviews']].values))
    data_compain = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == urltoLanding][['ga:campaign']].values))
    data_term = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == urltoLanding][['ga:keyword']].values))
    data_content = list(
        itertools.chain.from_iterable(df[df['ga:pagePath'] == urltoLanding][['ga:adContent']].values))
    slovartraf = dict(zip([data_namestraf[i]+' / '+ data_compain[i]+' / '+ data_term[i]+' / '+ data_content[i] for i in range(len(data_namestraf))], data_valuestraf))
    print(slovartraf)


    data = googleapi(slovartraf,df,urltoSuccess)
    data_names = list(data.keys())
    data_values = list(data.values())

    d = {'Источник': data_names, 'Количество': ['0' for x in data_values],'Сила': ['—' for x in data_values], 'Трафикфакт': [x[0] for x in data_values],
         'Конверсия': [str(int(x[1] / x[0] * 100)) + '%' if x[0] > 0 else x[0] for x in data_values],
         'Регистрациифакт': [x[1] for x in data_values], 'Бюджетплан': ['—' for x in data_values],
         'Бюджетфакт': ['—' for x in data_values]}


    resulttodf=pd.DataFrame(data=d)
    delete_zero_traf = resulttodf.drop(resulttodf[(resulttodf.Трафикфакт==0)].index)
    back_to_list=delete_zero_traf.to_dict(orient='list')
    return back_to_list




if __name__ == "__main__":
    # execute only if run as a script
    print(analitica_new_funnel([{'land': ['https://1.changellenge.com/supply-chain'], 'success': ['https://1.changellenge.com/supply-chain-success'], 'start': ['2019-08-30'], 'end': ['2019-10-30'], 'complete': ['complete'], 'heshteg': ['hash']}]))
