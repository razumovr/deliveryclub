from .models import Langing

import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe
import vk_api
import time
import datetime
import re


from rq import Queue
from worker import conn
from Startpage.utils import analitica,colvodneyforday
from Startpage.utils_new_funnel import analitica_new_funnel,colvodneyforday_new_funnel



from conecttosheets import connectsheet,connectIP,connect,connect_new_funnel


def googlesheets_new_funnel(completeurl,start,stop):
    df=connect_new_funnel(completeurl)
    df['new_col'] = df['utm_source'] + ' / ' + df['utm_medium']+ ' / ' + df['utm_campaign']+ ' / ' + df['utm_term']+ ' / ' + df['utm_content']
    a = df.dropna(subset=[list(df)[0]])
    newdf = a[['sended','utm_source', 'utm_medium', 'utm_campaign', 'new_col']]

    datedelta = []
    d1 = datetime.date(int(start[:4]), int(start[5:7]), int(start[8:10]))
    d2 = datetime.date(int(stop[:4]), int(stop[5:7]), int(stop[8:10]))


    dd = [d1 + datetime.timedelta(days=x) for x in range((d2 - d1).days + 1)]
    for x in dd:
        datedelta.append(str(x))



    #DELETE DATES
    for i in newdf['sended']:
        if i[:10] in datedelta or i==' ':
            pass
        else:
            newdf=newdf.drop(newdf.index[newdf['sended']==i])

    slovaritog = {'Уникальный пакет промо': 0,
                  'Уникальная рассылка': 0,
                  'Digest рассылка по всей базе': 0,
                  'Рассылка по сборному сегементу через mailchimp (например, те кто кликал на стажировки)': 0,
                  'Рассылка по сборной базе под конкретный проект (например, ИТшники из Уфы, 3-4 курс) или Рассылка по базе партнера чемпионата ': 0,
                  'рассылка по базе кейсеров': 0,
                  'рассылка по IT базе': 0,
                  'рассылка по базе инженеров': 0,
                  'рассылка по базе нефтяников': 0,
                  'рассылка по базе бизнес': 0,
                  'рассылка по базе partials': 0,
                  'Рассылка по новой базе hh': 0,
                  'Рассылка по базе курса первокурсника': 0,
                  'Рассылка по старой базе hh': 0,
                  'Рассылка по базе финансистов и экономистов': 0,
                  'Рассылка по базе менеджмента': 0,
                  'Рассылка по базе аналитиков': 0,
                  'рассылка по базе региона Спб': 0,
                  'рассылка по базе региона Сибирь': 0,
                  'рассылка по базе региона Урал': 0,
                  'рассылка по базе региона Волга': 0,
                  'рассылка по базе региона Дальний Восток': 0,
                  'рассылка по базе Казахстана': 0,
                  'рассылка по прошлогодней базе проекта': 0,
                  'рассылка по прошлогодней базе Аламни': 0,
                  'рассылка по прошлогодней базе Школы': 0,
                  'рассылка по прошлогодней базе Тулкита': 0,
                  'рассылка по прошлогодней базе стажировок': 0,
                  'рассылка по базе б2б партнеров (холодные)': 0,
                  'рассылка по базе б2б партнеров (теплые)': 0,
                  'таргетинг тизеры vk': 0,
                  'таргетинг в новостой ленте vk': 0,
                  'таргетинг в VK Stories': 0,
                  'таргетинг в новостой ленте instagram': 0,
                  'таргетинг в Instagram Stories': 0,
                  'таргетинг stories fb': 0,
                  'таргетинг в новостой ленте fb': 0,
                  'таргетинг на лидформу fb': 0,
                  'таргетинг на лидформу вк': 0,
                  'SMM:стена вк основная группа': 0,
                  'SMM:стена вк группа Спб': 0,
                  'SMM:стена вк группа Сибири': 0,
                  'SMM:стена вк группа Урала': 0,
                  'SMM:стена вк группа Волги': 0,
                  'SMM:стена вк группа Казахстана': 0,
                  'SMM:рассылка-дайжест ВК в ЛС': 0,
                  'SMM:рассылка о кейс-чемприонатах ВК в ЛС': 0,
                  'SMM:рассылка с вакансиями ВК в ЛС': 0,
                  'SMM:рассылка о мероприятиях ВК в ЛС': 0,
                  'SMM:рассылка со статьями/полезными материалами ВК в ЛС': 0,
                  'SMM:стена клиентской группы ВК': 0,
                  'пост в телеграм-канале': 0,
                  'дайджест в телеграм-канале': 0,
                  'ссылка на главном слайдере': 0,
                  'ссылка на главной в разделе мероприятий': 0,
                  'ссылка на главной в разделе обучения/курсов': 0,
                  'ссылка на главной в разделе чемпионатов': 0,
                  'пуш-уведомление на сайте': 0,
                  'ссылка на странице мероприятий': 0,
                  'ссылка на странице обучение': 0,
                  'ссылка на странице чемпионатов': 0,
                  'ссылка на странице вакансии': 0,
                  'поп-ап на сайте веб-версия': 0,
                  'поп-ап на сайте мобильная версия': 0,
                  'ссылка с личного кабинета': 0,
                  'Ссылка по роликом на Yotube-канал': 0,
                  'группа ФБ': 0,
                  'Страница АА в ФБ': 0,
                  'Страница в Твиттере': 0,
                  'ссылка в БИО': 0,
                  'ссылка в сториз': 0,
                  'инфопартнеры:баннер на сайте': 0,
                  'инфопартнеры:пост вконтакте': 0,
                  'инфопартнеры:пост в Telegram': 0,
                  'инфопартнеры:имейл рассылка': 0,
                  'инфопартнеры:статья или анонс на сайте': 0,
                  'инфопартнеры:пост в Twitter': 0,
                  'инфопартнеры:пост в Instagram': 0,
                  'инфопартнеры:пост в Facebook': 0,
                  'Амбассадор договаривается о размещении на онлайн-ресурсах': 0,
                  'Амбассадор собирает офлайн-регистрации': 0,
                  'Размещение в ЦРК': 0,
                  'Размещение в студсовете': 0,
                  'Размещение в профкоме': 0,
                  'Размещение в кейс-клубе': 0,
                  'Размещение в медиа': 0,
                  'Размещение в главной группе вуза': 0,
                  'Размещение для выпускников': 0,
                  'Размещение в бизнес-клубе': 0,
                  'Размещение на кафедре': 0,
                  'Размещение через преподавателей': 0,
                  'Размещение в студенческом научном обществе': 0,
                  'Размещение через онлайн-аутсорс': 0,
                  'Размещение через офлайн-аутсорс': 0,
                  'Роадшоу с флаерами/плакатами (регистрации по QR-коду)': 0,
                  'Роадшоу с анкетами (с дальнейшей оцифровкой)': 0,
                  'Размещение в СМИ': 0,
                  'прозвон по базе hh с отправкой рассылки': 0,
                  'Прозвон по partials с отправкой рассылки': 0,
                  'Прозвон по базам прошлых лет с отправкой рассылки': 0,
                  'Прозвон по каким-либо базам с отправкой рассылки': 0,
                  'Прозвон с регистрацией на звонке': 0,
                  'Яндекс на поиске по брендовым запросам': 0,
                  'Яндекс РСЯ по брендовым запросам': 0,
                  'Яндекс на Поиске по запросам без упоминания бренда': 0,
                  'Яндекс РСЯ по запросам без упоминания бренда': 0,
                  'Google на поиске по брендовым запросам': 0,
                  'Google КМС по брендовым запросам': 0,
                  'Google на Поиске по запросам без упоминания бренда': 0,
                  'Google КМС по запросам без упоминания бренда': 0,
                  'Youtube контекст': 0,
                  'Виртуальный рекрутер': 0,
                  'Органика': 0,
                  'Неопознанный трафик': 0}
    for k in list(newdf['new_col']):
        i = str(k)
        if 'all / changellenge / unical-promo' in i:
            slovaritog['Уникальный пакет промо'] += 1
        elif 'email / generalbase' in i:
            slovaritog['Уникальная рассылка'] += 1
        elif 'email / digest' in i:
            slovaritog['Digest рассылка по всей базе'] += 1
        elif 'email / segment-mailchimp' in i:
            slovaritog['Рассылка по сборному сегементу через mailchimp (например, те кто кликал на стажировки)'] += 1
        elif 'email / segment' in i:
            slovaritog['Рассылка по сборной базе под конкретный проект (например, ИТшники из Уфы, 3-4 курс) или Рассылка по базе партнера чемпионата '] += 1
        elif 'email / segment / cup' in i:
            slovaritog['рассылка по базе кейсеров'] += 1
        elif 'email / segment / it' in i:
            slovaritog['рассылка по IT базе'] += 1
        elif 'email / segment / engineers' in i:
            slovaritog['рассылка по базе инженеров'] += 1
        elif 'email / segment / oil' in i:
            slovaritog['рассылка по базе нефтяников']+= 1
        elif 'email / segment / business' in i:
            slovaritog['рассылка по базе бизнес'] += 1
        elif 'email / segment / partials' in i:
            slovaritog['рассылка по базе partials'] += 1
        elif 'email / segment / external' in i:
            slovaritog['Рассылка по новой базе hh'] += 1




        elif 'email / segment / kp' in i:
            slovaritog['Рассылка по базе курса первокурсника']+= 1
        elif 'email / segment / old-external' in i:
            slovaritog['Рассылка по старой базе hh'] += 1
        elif 'email / segment / fin' in i:
            slovaritog['Рассылка по базе финансистов и экономистов']+= 1
        elif 'email / segment / manager' in i:
            slovaritog['Рассылка по базе менеджмента'] += 1
        elif 'email / segment / analytic' in i:
            slovaritog['Рассылка по базе аналитиков'] += 1
        elif 'email / segment / spb' in i:
            slovaritog['рассылка по базе региона Спб'] += 1
        elif 'email / segment / siberia' in i:
            slovaritog['рассылка по базе региона Сибирь']+= 1
        elif 'eemail / segment / ural' in i:
            slovaritog['рассылка по базе региона Урал'] += 1
        elif 'email / segment / volga' in i:
            slovaritog['рассылка по базе региона Волга'] += 1
        elif 'email / segment / dv' in i:
            slovaritog['рассылка по базе региона Дальний Восток'] += 1
        elif 'email / segment / kz' in i:
            slovaritog['рассылка по базе Казахстана'] += 1
        elif 'email / segment / last-year' in i:
            slovaritog['рассылка по прошлогодней базе проекта'] += 1
        elif 'email / segment / alumni' in i:
            slovaritog['рассылка по прошлогодней базе Аламни'] += 1
        elif 'email / segment / school' in i:
            slovaritog['рассылка по прошлогодней базе Школы'] += 1
        elif 'email / segment / toolkit' in i:
            slovaritog['рассылка по прошлогодней базе Тулкита'] += 1
        elif 'email / segment / internship' in i:
            slovaritog['рассылка по прошлогодней базе стажировок'] += 1
        elif 'email / hr-digest / cold' in i:
            slovaritog['рассылка по базе б2б партнеров (холодные)'] += 1
        elif 'email / hr-digest / warm' in i:
            slovaritog['рассылка по базе б2б партнеров (теплые)'] += 1
        elif 'target / vk / tizer' in i:
            slovaritog['таргетинг тизеры vk'] += 1
        elif 'target / vk / post' in i:
            slovaritog['таргетинг в новостой ленте vk'] += 1
        elif 'target / vk / story' in i:
            slovaritog['таргетинг в VK Stories'] += 1
        elif 'target / insta / post' in i:
            slovaritog['таргетинг в новостой ленте instagramа']+= 1
        elif 'target / insta / story' in i:
            slovaritog['таргетинг в Instagram Stories']+= 1
        elif 'target / fb / story' in i:
            slovaritog['таргетинг stories fb'] += 1
        elif 'target / fb / post' in i:
            slovaritog['таргетинг в новостой ленте fb'] += 1
        elif 'target / fb / leadform' in i:
            slovaritog['таргетинг на лидформу fb'] += 1
        elif 'target / vk / leadform' in i:
            slovaritog['таргетинг на лидформу вк'] += 1
        elif 'vk / global / post' in i:
            slovaritog['SMM:стена вк основная группа'] += 1
        elif 'vk / spb / post' in i:
            slovaritog['SMM:стена вк группа Спб'] += 1
        elif 'vk / siberia / post' in i:
            slovaritog['SMM:стена вк группа Сибири'] += 1
        elif 'vk / ural / post' in i:
            slovaritog['SMM:стена вк группа Урала'] += 1
        elif 'vk / volga / post' in i:
            slovaritog['SMM:стена вк группа Волги'] += 1
        elif 'vk / kz / post' in i:
            slovaritog['SMM:стена вк группа Казахстана'] += 1
        elif 'vk / global / digest' in i:
            slovaritog['SMM:рассылка-дайжест ВК в ЛС'] += 1
        elif 'vk / global / cups' in i:
            slovaritog['SMM:рассылка о кейс-чемприонатах ВК в ЛС'] += 1
        elif 'vk / global / vacancy' in i:
            slovaritog['SMM:рассылка с вакансиями ВК в ЛС'] += 1
        elif 'vk / global / events' in i:
            slovaritog['SMM:рассылка о мероприятиях ВК в ЛС'] += 1
        elif 'vk / global / article' in i:
            slovaritog['SMM:рассылка со статьями/полезными материалами ВК в ЛС'] += 1
        elif 'vk / ' in i and 'post / (not set)' in i:
            slovaritog['SMM:стена клиентской группы ВК'] += 1
        elif 'tg / post' in i:
            slovaritog['пост в телеграм-канале'] += 1
        elif 'tg / digest' in i:
            slovaritog['дайджест в телеграм-канале'] += 1
        elif 'cl-site / main / slider' in i:
            slovaritog['ссылка на главном слайдере'] += 1
        elif 'cl-site / main / events' in i:
            slovaritog['ссылка на главной в разделе мероприятий'] += 1
        elif 'cl-site / main / education' in i:
            slovaritog['ссылка на главной в разделе обучения/курсов'] += 1
        elif 'cl-site / main / champs' in i:
            slovaritog['ссылка на главной в разделе чемпионатов'] += 1
        elif 'cl-site / push' in i:
            slovaritog['пуш-уведомление на сайте'] += 1
        elif 'cl-site / page / event' in i:
            slovaritog['ссылка на странице мероприятий'] += 1
        elif 'cl-site / page / education' in i:
            slovaritog['ссылка на странице обучение'] += 1
        elif 'cl-site / page / champs' in i:
            slovaritog['ссылка на странице чемпионатов'] += 1
        elif 'cl-site / page / vacancy' in i:
            slovaritog['ссылка на странице вакансии'] += 1
        elif 'cl-site / popup / desktop' in i:
            slovaritog['поп-ап на сайте веб-версия'] += 1
        elif 'cl-site / popup / mobile' in i:
            slovaritog['поп-ап на сайте мобильная версия'] += 1
        elif 'cl-site / main / personal' in i:
            slovaritog['ссылка с личного кабинета'] += 1
        elif 'youtube / video' in i:
            slovaritog['Ссылка по роликом на Yotube-канал'] += 1
        elif 'fb / post' in i:
            slovaritog['группа ФБ'] += 1
        elif 'fb / post / aa' in i:
            slovaritog['Страница АА в ФБ'] += 1
        elif 'twitter / post / aa' in i:
            slovaritog['Страница в Твиттере'] += 1
        elif 'inst / bio' in i:
            slovaritog['ссылка в БИО'] += 1
        elif 'inst / stories' in i:
            slovaritog['ссылка в сториз'] += 1
        elif 'ip /' in i and 'banner /' in i:
            slovaritog['инфопартнеры:баннер на сайте'] += 1
        elif 'ip /' in i and 'vk-post /' in i:
            slovaritog['инфопартнеры:пост вконтакте'] += 1
        elif 'ip /' in i and 'tg-post /' in i:
            slovaritog['инфопартнеры:пост в Telegram'] += 1
        elif 'ip /' in i and 'email /' in i:
            slovaritog['инфопартнеры:имейл рассылка'] += 1
        elif 'ip /' in i and 'article /' in i:
            slovaritog['инфопартнеры:статья или анонс на сайте'] += 1
        elif 'ip /' in i and 'tw-post /' in i:
            slovaritog['инфопартнеры:пост в Twitter'] += 1
        elif 'ip /' in i and 'inst-post /' in i:
            slovaritog['инфопартнеры:пост в Instagram'] += 1
        elif 'ip /' in i and 'fb-post /' in i:
            slovaritog['инфопартнеры:пост в Facebook'] += 1
        elif 'amb /' in i and 'online /' in i:
            slovaritog['Амбассадор договаривается о размещении на онлайн-ресурсах'] += 1
        elif 'amb /' in i and 'offline /' in i:
            slovaritog['Амбассадор собирает офлайн-регистрации'] += 1
        elif 'vuz /' in i and 'crk / chat /' in i:
            slovaritog['Размещение в ЦРК'] += 1
        elif 'vuz /' in i and 'studsovet / vk-post /' in i:
            slovaritog['Размещение в студсовете'] += 1
        elif 'vuz /' in i and 'profkom / fb-post /' in i:
            slovaritog['Размещение в профкоме'] += 1
        elif 'vuz /' in i and 'kk / website /' in i:
            slovaritog['Размещение в кейс-клубе'] += 1
        elif 'vuz /' in i and 'media / email /' in i:
            slovaritog['Размещение в медиа'] += 1
        elif 'vuz /' in i and 'maingroup / article /' in i:
            slovaritog['Размещение в главной группе вуза'] += 1
        elif 'vuz /' in i and 'alumni / webinar /' in i:
            slovaritog['Размещение для выпускников'] += 1
        elif 'vuz /' in i and 'bk /' in i:
            slovaritog['Размещение в бизнес-клубе'] += 1
        elif 'vuz /' in i and 'kafedra /' in i:
            slovaritog['Размещение на кафедре'] += 1
        elif 'vuz /' in i and 'teacher /' in i:
            slovaritog['Размещение через преподавателей'] += 1
        elif 'vuz /' in i and 'sno /' in i:
            slovaritog['Размещение в студенческом научном обществе'] += 1
        elif 'vuz /' in i and 'online-outsors /' in i:
            slovaritog['Размещение через онлайн-аутсорс'] += 1
        elif 'vuz /' in i and 'offline-outsors /' in i:
            slovaritog['Размещение через офлайн-аутсорс'] += 1
        elif 'vuz /' in i and 'flyer /' in i:
            slovaritog['Роадшоу с флаерами/плакатами (регистрации по QR-коду)'] += 1
        elif 'vuz /' in i and 'roadshow /' in i:
            slovaritog['Роадшоу с анкетами (с дальнейшей оцифровкой)'] += 1
        elif 'smi /' in i and '(not set) / (not set)' in i:
            slovaritog['Размещение в СМИ '] += 1
        elif 'tlm / email / external' in i:
            slovaritog['прозвон по базе hh с отправкой рассылки'] += 1
        elif 'tlm / email / partials' in i:
            slovaritog['Прозвон по partials с отправкой рассылки'] += 1
        elif 'tlm / email / last-year' in i:
            slovaritog['Прозвон по базам прошлых лет с отправкой рассылки'] += 1
        elif 'tlm / email' in i:
            slovaritog['Прозвон по каким-либо базам с отправкой рассылки'] += 1
        elif 'tlm / reg' in i:
            slovaritog['Прозвон с регистрацией на звонке'] += 1
        elif 'yandex / cpc' in i and 'brand' in i:
            slovaritog['Яндекс на поиске по брендовым запросам'] += 1
        elif 'yandex / cpm' in i and 'brand' in i:
            slovaritog['Яндекс РСЯ по брендовым запросам'] += 1
        elif 'yandex / cpc' in i and 'general' in i:
            slovaritog['Яндекс на Поиске по запросам без упоминания бренда'] += 1
        elif 'yandex / cpm' in i and 'general' in i:
            slovaritog['Яндекс РСЯ по запросам без упоминания бренда'] += 1
        elif 'google / cpc' in i and 'brand' in i:
            slovaritog['Google на поиске по брендовым запросам'] += 1
        elif 'google / cpm' in i and 'brand' in i:
            slovaritog['Google КМС по брендовым запросам'] += 1
        elif 'google / cpc' in i and 'general' in i:
            slovaritog['Google на Поиске по запросам без упоминания бренда'] += 1
        elif 'google / cpm' in i and 'general' in i:
            slovaritog['Google КМС по запросам без упоминания бренда'] += 1
        elif 'youtube / cpm' in i and 'brand' in i:
            slovaritog['Youtube контекст'] += 1
        elif 'external-lidgen / cpc / premium' in i:
            slovaritog['Виртуальный рекрутер'] += 1
        elif '(direct) / (none)' in i or 'referral' in i or 'organic' in i:
            slovaritog['Органика'] += 1
        else:
            slovaritog['Неопознанный трафик'] += 1



    return dict((k, v) for k, v in slovaritog.items() if v!=0)

def googlesheets(completeurl,start,stop):
    df=connect(completeurl)
    df['new_col'] = df['utm_source'] + ' / ' + df['utm_medium']
    a = df.dropna(subset=[list(df)[0]])
    newdf = a[['sended','utm_source', 'utm_medium', 'utm_campaign', 'new_col']]


    datedelta = []
    d1 = datetime.date(int(start[:4]), int(start[5:7]), int(start[8:10]))
    d2 = datetime.date(int(stop[:4]), int(stop[5:7]), int(stop[8:10]))


    dd = [d1 + datetime.timedelta(days=x) for x in range((d2 - d1).days + 1)]
    for x in dd:
        datedelta.append(str(x))



    #DELETE DATES
    for i in newdf['sended']:
        if i[:10] in datedelta or i==' ':
            pass
        else:
            newdf=newdf.drop(newdf.index[newdf['sended']==i])
    print(newdf)

    slovaritog = {'Уникальная': 0, 'Дайджест': 0, 'SMM репостов': 0,
                  'Инфопартнеры':0, 'Рассылка из юнисендера': 0, 'Промо в вузах': 0, 'Телеграм': 0,
                  'Таргетинг': 0,
                  'Веб-страница и слайдер': 0, 'Контекстная реклама': 0, 'Органика':0, 'Неопознанный трафик': 0}
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
        elif 'vk / target' in ii or 'vk / targetpost' in ii or 'vk / target-story' in ii or 'insta / target' in ii or 'insta / targetpost' in ii or 'insta / target-story' in ii or 'fb / target' in ii or 'fb / targetpost' in ii or 'target' in ii:
            slovaritog['Таргетинг'] += 1
        elif 'cl-site' in ii or 'Сl-site' in ii or 'cl_site' in ii or 'Сl_site' in ii:
            slovaritog['Веб-страница и слайдер'] += 1
        elif 'google / cpc' in ii or 'youtube / instream' in ii or 'yandex / cpc' in ii:
            slovaritog['Контекстная реклама'] += 1
        elif i==' / ':
            slovaritog['Органика'] += 1
        else:
            slovaritog['Неопознанный трафик'] += 1

    return slovaritog

def infopartnerip(urlland,start,stop):
    dfip=connectIP('https://docs.google.com/spreadsheets/d/1WmDnz3794uoU_h7ho_hOPMISUA2CdXt_UA_8L9pcJ-s/edit?pli=1#gid=0')
    costdf = dfip[dfip.values == urlland].loc[:,['Дата выдачи','Стоимость ']]
    datedelta = []
    d1 = datetime.date(int(start[:4]), int(start[5:7]), int(start[8:10]))
    d2 = datetime.date(int(stop[:4]), int(stop[5:7]), int(stop[8:10]))


    # this will give you a list containing all of the dates
    dd = [d1 + datetime.timedelta(days=x) for x in range((d2 - d1).days + 1)]
    for x in dd:
        datedelta.append(str(x))

    for i in range(len(datedelta)):
        datedelta[i]=datetime.date(int(datedelta[i][:4]), int(datedelta[i][5:7]), int(datedelta[i][8:10])).strftime("%d.%m.%Y")

    costdfprice=[]
    for i in costdf.index:
        if costdf.loc[i,'Дата выдачи'] in datedelta:
            costdfprice.append(costdf.loc[i,'Стоимость '])
    costdfpriceinint = [int(item) for item in costdfprice if item.isdigit()==True]
    ipKOLICHESTVO = len(costdfprice)
    sumcostdf = sum(costdfpriceinint)
    return [ipKOLICHESTVO,sumcostdf]



def SMMcountfunct(start,stop,urlland):
    '''
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
            newwww.append(SMMM['items'][i]['id'])'''


    dfip=connectIP('https://docs.google.com/spreadsheets/d/1WBPvHdGxyaqzFwKAskt_CFq9rTdMGHnQMc-Dr9MVNwE/edit#gid=0')
    costdf = dfip[dfip.values == urlland].loc[:,['Дата старта промо','Ссылка на пост']]
    datedelta = []
    d1 = datetime.date(int(start[:4]), int(start[5:7]), int(start[8:10]))
    d2 = datetime.date(int(stop[:4]), int(stop[5:7]), int(stop[8:10]))


    # this will give you a list containing all of the dates
    dd = [d1 + datetime.timedelta(days=x) for x in range((d2 - d1).days + 1)]
    for x in dd:
        datedelta.append(str(x))

    for i in range(len(datedelta)):
        datedelta[i]=datetime.date(int(datedelta[i][:4]), int(datedelta[i][5:7]), int(datedelta[i][8:10])).strftime("%d.%m.%Y")

    urltopost=[]
    for i in costdf.index:
        if costdf.loc[i,'Дата старта промо'] in datedelta:
            numberpost=re.search(r'[_].+',costdf.loc[i,'Ссылка на пост']).group(0)[1:]
            if numberpost.isdigit():
                urltopost.append(int(numberpost))

    vk_session = vk_api.VkApi('+79055106387', '#rr7363446909250797rr##')
    vk_session.auth()
    vk = vk_session.get_api()
    idreposts = []
    for i in urltopost:
        slova = vk.wall.getReposts(owner_id=-25758, post_id=i, count=1000)
        for i in range(len(slova['items'])):
            if slova['items'][i]['from_id'] < 0:
                idreposts.append(slova['items'][i]['from_id'])

    return len(idreposts)



def main():
    landing = Langing.objects.all()
    dictItog={}

    q = Queue(connection=conn)

    result = q.enqueue(analitica,str(landing[0].land),str(landing[0].success),str(landing[0].start),str(landing[0].end))
    result1 = q.enqueue(colvodneyforday,str(landing[0].start),str(landing[0].end),str(landing[0].land))
    try:
        connecttocomplete = googlesheets(str(landing[0].complete),str(landing[0].start),str(landing[0].end))
    except:
        connecttocomplete={}


    try:
        connecttargeting = connectsheet('https://docs.google.com/spreadsheets/d/1lcHMPIw1AtzKx3DoFAVp_JDi2Cb_-DbP9krjtD7c69Q/edit#gid=237212384',str(landing[0].start),str(landing[0].land))
    except:
        connecttargeting={}


    try:
        
        
        infopartenrilist=infopartnerip(str(landing[0].land),str(landing[0].start),str(landing[0].end))
    except:
        infopartenrilist={}


    try:
        SMMcount=SMMcountfunct(str(landing[0].start),str(landing[0].end),str(landing[0].land))
    except:
        SMMcount=0
    #time.sleep(5)

    print("REZULT"*100)
    print(result.result)
    print(result1.result)
    print(connecttargeting)
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
        dictItog['Конверсия']=[str(int(dictItog['Регистрациифакт'][i]/dictItog['Трафикфакт'][i]*100))+'%' if dictItog['Трафикфакт'][i]!=0 else '0%' for i in range(len(dictItog['Источник']))]
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
        dictItog['Количество'][10]=result1.result[3]
    except:
        pass
    try:
        dictItog['Количество'][0]=result1.result[4]
    except:
        pass
    try:
        dictItog['Количество'][1]=result1.result[5]
    except:
        pass
    try:
        dictItog['Количество'][6]=result1.result[6]
    except:
        pass
    try:
        dictItog['Трафикфакт'][7]=connecttargeting['Трафикфакт']
    except:
        pass
    try:
        dictItog['Бюджетплан'][7]=connecttargeting['Бюджетплан']
    except:
        pass
    try:
        dictItog['Бюджетфакт'][7]=connecttargeting['Бюджетфакт']
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
    print(dictItog)
    print('-'*100)
    a=[]
    try:
        for i in range(len(dictItog['Трафикфакт'])):
            if int(dictItog['Количество'][i])!=0:
                a.append(int(int(dictItog['Трафикфакт'][i]) / int(dictItog['Количество'][i])))
            else:
                a.append('—')
        dictItog["Сила"]=a
    except:
        pass
    #ITOGO
    dictItog['Источник'].append('Итого')
    dictItog['Количество'].append('—')
    dictItog['Сила'].append('—')
    dictItog['Трафикфакт'].append(sum([int(item) for item in dictItog['Трафикфакт']]))
    dictItog['Регистрациифакт'].append(sum([int(item) for item in dictItog['Регистрациифакт']]))
    if dictItog['Трафикфакт'][-1]!=0:
        dictItog['Конверсия'].append(str(int(dictItog['Регистрациифакт'][-1]/dictItog['Трафикфакт'][-1]*100))+'%')
    else:
        dictItog['Конверсия'].append('0%')
    dictItog['Бюджетплан'].append('—')
    dictItog['Бюджетфакт'].append('—')
    print(dictItog)
    return dictItog


def main_for_new_funnel():
    dictItog = {}
    name_utm={
    'Уникальный пакет промо': 'all / changellenge / unical-promo',
     'Уникальная рассылка': 'email / generalbase',
     'Digest рассылка по всей базе': 'email / digest',
     'Рассылка по сборному сегементу через mailchimp (например, те кто кликал на стажировки)': 'email / segment-mailchimp',
     'Рассылка по сборной базе под конкретный проект (например, ИТшники из Уфы, 3-4 курс) или Рассылка по базе партнера чемпионата ': 'email / segment',
     'рассылка по базе кейсеров': 'email / segment / cup',
     'рассылка по IT базе': 'email / segment / it',
     'рассылка по базе инженеров': 'email / segment / engineers',
     'рассылка по базе нефтяников': 'email / segment / oil',
     'рассылка по базе бизнес': 'email / segment / business',
     'рассылка по базе partials': 'email / segment / partials',
     'Рассылка по новой базе hh': 'email / segment / external',
     'Рассылка по базе курса первокурсника': 'email / segment / kp',
     'Рассылка по старой базе hh': 'email / segment / old-external',
     'Рассылка по базе финансистов и экономистов': 'email / segment / fin',
     'Рассылка по базе менеджмента': 'email / segment / manager',
     'Рассылка по базе аналитиков': 'email / segment / analytic',
     'рассылка по базе региона Спб': 'email / segment / spb',
     'рассылка по базе региона Сибирь': 'email / segment / siberia',
     'рассылка по базе региона Урал': 'email / segment / ural',
     'рассылка по базе региона Волга': 'email / segment / volga',
     'рассылка по базе региона Дальний Восток': 'email / segment / dv',
     'рассылка по базе Казахстана': 'email / segment / kz',
     'рассылка по прошлогодней базе проекта': 'email / segment / last-year',
     'рассылка по прошлогодней базе Аламни': 'email / segment / alumni',
     'рассылка по прошлогодней базе Школы': 'email / segment / school',
     'рассылка по прошлогодней базе Тулкита': 'email / segment / toolkit',
     'рассылка по прошлогодней базе стажировок': 'email / segment / internship',
     'рассылка по базе б2б партнеров (холодные)': 'email / hr-digest / cold',
     'рассылка по базе б2б партнеров (теплые)': 'email / hr-digest / warm',
     'таргетинг тизеры vk': 'target / vk / tizer',
     'таргетинг в новостой ленте vk': 'target / vk / post',
     'таргетинг в VK Stories': 'target / vk / story',
     'таргетинг в новостой ленте instagram': 'target / insta / post',
     'таргетинг в Instagram Stories': 'target / insta / story',
     'таргетинг stories fb': 'target / fb / story',
     'таргетинг в новостой ленте fb': 'target / fb / post',
     'таргетинг на лидформу fb': 'target / fb / leadform',
     'таргетинг на лидформу вк': 'target / vk / leadform',
     'SMM:стена вк основная группа': 'vk / global / post',
     'SMM:стена вк группа Спб': 'vk / spb / post',
     'SMM:стена вк группа Сибири': 'vk / siberia / post',
     'SMM:стена вк группа Урала': 'vk / ural / post',
     'SMM:стена вк группа Волги': 'vk / volga / post',
     'SMM:стена вк группа Казахстана': 'vk / kz / post',
     'SMM:рассылка-дайжест ВК в ЛС': 'vk / global / digest',
     'SMM:рассылка о кейс-чемприонатах ВК в ЛС': 'vk / global / cups',
     'SMM:рассылка с вакансиями ВК в ЛС': 'vk / global / vacancy',
     'SMM:рассылка о мероприятиях ВК в ЛС': 'vk / global / events',
     'SMM:рассылка со статьями/полезными материалами ВК в ЛС': 'vk / global / article',
     'SMM:стена клиентской группы ВК':  'post / (not set)',
     'пост в телеграм-канале': 'tg / post',
     'дайджест в телеграм-канале': 'tg / digest',
     'ссылка на главном слайдере': 'cl-site / main / slider',
     'ссылка на главной в разделе мероприятий': 'cl-site / main / events',
     'ссылка на главной в разделе обучения/курсов': 'cl-site / main / education',
     'ссылка на главной в разделе чемпионатов': 'cl-site / main / champs',
     'пуш-уведомление на сайте': 'cl-site / push',
     'ссылка на странице мероприятий': 'cl-site / page / event',
     'ссылка на странице обучение': 'cl-site / page / education',
     'ссылка на странице чемпионатов': 'cl-site / page / champs',
     'ссылка на странице вакансии': 'cl-site / page / vacancy',
     'поп-ап на сайте веб-версия': 'cl-site / popup / desktop',
     'поп-ап на сайте мобильная версия': 'cl-site / popup / mobile',
     'ссылка с личного кабинета': 'cl-site / main / personal',
     'Ссылка по роликом на Yotube-канал': 'youtube / video',
     'группа ФБ': 'fb / post',
     'Страница АА в ФБ': 'fb / post / aa',
     'Страница в Твиттере': 'twitter / post / aa',
     'ссылка в БИО': 'inst / bio',
     'ссылка в сториз': 'inst / stories',
     'инфопартнеры:баннер на сайте': 'ip / banner',
     'инфопартнеры:пост вконтакте': 'ip / vk-post',
     'инфопартнеры:пост в Telegram': 'ip / tg-post',
     'инфопартнеры:имейл рассылка': 'ip / email',
     'инфопартнеры:статья или анонс на сайте': 'ip / article',
     'инфопартнеры:пост в Twitter': 'ip / tw-post',
     'инфопартнеры:пост в Instagram': 'ip / inst-post',
     'инфопартнеры:пост в Facebook': 'ip / fb-post',
     'Амбассадор договаривается о размещении на онлайн-ресурсах': 'amb / online',
     'Амбассадор собирает офлайн-регистрации': 'amb / offline',
     'Размещение в ЦРК': 'vuz / crk',
     'Размещение в студсовете': 'vuz / studsovet',
     'Размещение в профкоме': 'vuz / profkom',
     'Размещение в кейс-клубе': 'vuz / kk',
     'Размещение в медиа': 'vuz / media',
     'Размещение в главной группе вуза': 'vuz / maingroup',
     'Размещение для выпускников':'vuz / alumni',
     'Размещение в бизнес-клубе': 'vuz / bk',
     'Размещение на кафедре': 'vuz / kafedra',
     'Размещение через преподавателей': 'vuz / teacher',
     'Размещение в студенческом научном обществе': 'vuz / sno',
     'Размещение через онлайн-аутсорс': 'vuz / online-outsors',
     'Размещение через офлайн-аутсорс': 'vuz / offline-outsors',
     'Роадшоу с флаерами/плакатами (регистрации по QR-коду)': 'vuz / flyer',
     'Роадшоу с анкетами (с дальнейшей оцифровкой)': 'vuz / roadshow',
     'Размещение в СМИ': 'smi /',
     'прозвон по базе hh с отправкой рассылки': 'tlm / email / external',
     'Прозвон по partials с отправкой рассылки': 'tlm / email / partials',
     'Прозвон по базам прошлых лет с отправкой рассылки': 'tlm / email / last-year',
     'Прозвон по каким-либо базам с отправкой рассылки': 'tlm / email',
     'Прозвон с регистрацией на звонке': 'tlm / reg',
     'Яндекс на поиске по брендовым запросам': 'yandex / cpc / brand',
     'Яндекс РСЯ по брендовым запросам': 'yandex / cpm / brand',
     'Яндекс на Поиске по запросам без упоминания бренда': 'yandex / cpc / general',
     'Яндекс РСЯ по запросам без упоминания бренда': 'yandex / cpm / general',
     'Google на поиске по брендовым запросам': 'google / cpc / brand',
     'Google КМС по брендовым запросам': 'google / cpm / brand',
     'Google на Поиске по запросам без упоминания бренда': 'google / cpc / general',
     'Google КМС по запросам без упоминания бренда': 'google / cpm / general',
     'Youtube контекст': 'youtube / cpm / general',
     'Виртуальный рекрутер': 'external-lidgen / cpc / premium',
     'Органика': '(direct) / (none)',

    }
    landing = Langing.objects.all()


    q = Queue(connection=conn)
    result =q.enqueue(analitica_new_funnel,str(landing[0].land), str(landing[0].success), str(landing[0].start),str(landing[0].end))


    result1=q.enqueue(colvodneyforday_new_funnel,str(landing[0].start), str(landing[0].end), str(landing[0].land))




    try:
        connecttocomplete = googlesheets_new_funnel(str(landing[0].complete), str(landing[0].start), str(landing[0].end))
    except:
        connecttocomplete = {}


    try:
        connecttargeting = connectsheet(
            'https://docs.google.com/spreadsheets/d/1lcHMPIw1AtzKx3DoFAVp_JDi2Cb_-DbP9krjtD7c69Q/edit#gid=237212384',
            str(landing[0].start), str(landing[0].land))
    except:
        connecttargeting = {}

    try:

        infopartenrilist = infopartnerip(str(landing[0].land), str(landing[0].start), str(landing[0].end))
    except:
        infopartenrilist = {}

    try:
        SMMcount = SMMcountfunct(str(landing[0].start), str(landing[0].end), str(landing[0].land))
    except:
        SMMcount = 0
    #time.sleep(15)

    print("!" * 100)
    print(result.result)
    print("!" * 100)
    print(result1.result)
    print("!" * 100)
    print(connecttocomplete)
    print("!" * 100)
    print(connecttargeting)
    print("!" * 100)
    print(infopartenrilist)
    print("!" * 100)
    print(SMMcount)
    print("!" * 100)


    #Concat analitica+colichestvo
    if result1.result is not None:
        for i in range(len(result.result['Источник'])-1):
            result.result['Количество'][i]=result1.result[name_utm[result.result['Источник'][i]]]



    dictItog = result.result

    connecttocompleteresult = connecttocomplete
    if bool(connecttocompleteresult) == True:
        for i in dictItog['Источник']:
            if i in connecttocomplete:
                dictItog['Регистрациифакт'][dictItog['Источник'].index(i)]=connecttocomplete[i]
            else:
                dictItog['Регистрациифакт'][dictItog['Источник'].index(i)]=0
        dictItog['Конверсия'] = [str(int(dictItog['Регистрациифакт'][i] / dictItog['Трафикфакт'][i] * 100)) + '%' if dictItog['Трафикфакт'][i] != 0 else '0%'for i in range(len(dictItog['Источник']))]
    else:
        pass


    if bool(connecttargeting) == True:
        for i in dictItog['Источник']:
            indexnumber=None
            if 'таргетинг' in i:
                indexnumber=dictItog['Источник'].index(i)
                break

        dictItog['Источник']=dictItog['Источник'][:indexnumber]+['Таргетинг общая информация']+dictItog['Источник'][indexnumber:]
        dictItog['Количество']=dictItog['Количество'][:indexnumber]+[0]+dictItog['Количество'][indexnumber:]
        dictItog['Сила']=dictItog['Сила'][:indexnumber]+['—']+dictItog['Сила'][indexnumber:]
        dictItog['Трафикфакт']=dictItog['Трафикфакт'][:indexnumber]+[connecttargeting['Трафикфакт']]+dictItog['Трафикфакт'][indexnumber:]
        dictItog['Регистрациифакт']=dictItog['Регистрациифакт'][:indexnumber]+[connecttargeting['Регистрациифакт']]+dictItog['Регистрациифакт'][indexnumber:]
        dictItog['Бюджетплан']=dictItog['Бюджетплан'][:indexnumber]+[connecttargeting['Бюджетплан']]+dictItog['Бюджетплан'][indexnumber:]
        dictItog['Бюджетфакт']=dictItog['Бюджетфакт'][:indexnumber]+[connecttargeting['Бюджетфакт']]+dictItog['Бюджетфакт'][indexnumber:]
        dictItog['Конверсия']=dictItog['Конверсия'][:indexnumber]+[connecttargeting['Конверсия']]+dictItog['Конверсия'][indexnumber:]


    if bool(infopartenrilist) == True:
        for i in dictItog['Источник']:
            indexnumber=None
            if 'инфопартнеры:' in i:
                indexnumber=dictItog['Источник'].index(i)
                break

        number_infopartenrilist_in_dict = 0
        for i in dictItog['Источник']:
            if 'инфопартнеры:' in i:
                number_infopartenrilist_in_dict+=1

        dictItog['Источник']=dictItog['Источник'][:indexnumber]+['Инфопартнеры общая информация']+dictItog['Источник'][indexnumber:]
        dictItog['Количество']=dictItog['Количество'][:indexnumber]+[infopartenrilist[0]]+dictItog['Количество'][indexnumber:]
        dictItog['Трафикфакт']=dictItog['Трафикфакт'][:indexnumber]+[sum([int(x) for x in dictItog['Трафикфакт'][indexnumber:indexnumber+number_infopartenrilist_in_dict]])]+dictItog['Трафикфакт'][indexnumber:]
        dictItog['Сила']=dictItog['Сила'][:indexnumber]+['—']+dictItog['Сила'][indexnumber:]
        dictItog['Регистрациифакт']=dictItog['Регистрациифакт'][:indexnumber]+[sum([int(x) for x in dictItog['Регистрациифакт'][indexnumber:indexnumber+number_infopartenrilist_in_dict]])]+dictItog['Регистрациифакт'][indexnumber:]
        dictItog['Бюджетплан']=dictItog['Бюджетплан'][:indexnumber]+['—']+dictItog['Бюджетплан'][indexnumber:]
        dictItog['Бюджетфакт']=dictItog['Бюджетфакт'][:indexnumber]+[infopartenrilist[1]]+dictItog['Бюджетфакт'][indexnumber:]
        dictItog['Конверсия']=dictItog['Конверсия'][:indexnumber]+['—']+dictItog['Конверсия'][indexnumber:]

    if SMMcount!=0:
        for i in dictItog['Источник']:
            indexnumber=None
            if 'SMM:' in i:
                indexnumber=dictItog['Источник'].index(i)
                break

        number_SMM_in_dict = 0
        for i in dictItog['Источник']:
            if 'SMM:' in i:
                number_SMM_in_dict+=1

        dictItog['Источник']=dictItog['Источник'][:indexnumber]+['SMM общая информация']+dictItog['Источник'][indexnumber:]
        dictItog['Количество']=dictItog['Количество'][:indexnumber]+[SMMcount]+dictItog['Количество'][indexnumber:]
        dictItog['Трафикфакт']=dictItog['Трафикфакт'][:indexnumber]+[sum([int(x) for x in dictItog['Трафикфакт'][indexnumber:indexnumber+number_SMM_in_dict]])]+dictItog['Трафикфакт'][indexnumber:]
        dictItog['Сила']=dictItog['Сила'][:indexnumber]+['—']+dictItog['Сила'][indexnumber:]
        dictItog['Регистрациифакт']=dictItog['Регистрациифакт'][:indexnumber]+[sum([int(x) for x in dictItog['Регистрациифакт'][indexnumber:indexnumber+number_SMM_in_dict]])]+dictItog['Регистрациифакт'][indexnumber:]
        dictItog['Бюджетплан']=dictItog['Бюджетплан'][:indexnumber]+['—']+dictItog['Бюджетплан'][indexnumber:]
        dictItog['Бюджетфакт']=dictItog['Бюджетфакт'][:indexnumber]+['—']+dictItog['Бюджетфакт'][indexnumber:]
        dictItog['Конверсия']=dictItog['Конверсия'][:indexnumber]+['—']+dictItog['Конверсия'][indexnumber:]

    #Сила
    a=[]
    try:
        for i in range(len(dictItog['Трафикфакт'])):
            if int(dictItog['Количество'][i])!=0:
                a.append(int(int(dictItog['Трафикфакт'][i]) / int(dictItog['Количество'][i])))
            else:
                a.append('—')
        dictItog["Сила"]=a
    except:
        pass

    print(dictItog)

    return dictItog



if __name__ == "__main__":
    # execute only if run as a script
    main()
