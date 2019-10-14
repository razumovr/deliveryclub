from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Person, City, Country, Firstvar, Urlname
from .forms import PersonForm, FirstForm, SecondForm, ThirdForm, UrlForm
from .conecttosheets import Connection, UTMtable, PSP
import urllib.parse as urlparse
import os
import psycopg2
from django.shortcuts import redirect


import pandas as pd
import re
import cyrtranslit
import urllib.request as urllib2
import urllib.parse

gs = Connection()
gs.connect()
utm = UTMtable(gs.service)
b = utm.getSheets()
c = utm.tables.keys()
k = utm.tables


def insertinsql():
    try:
        Person.objects.all().delete()
    except:
        pass
    try:
        City.objects.all().delete()
    except:
        pass
    try:
        Country.objects.all().delete()
    except:
        pass
    try:
        Firstvar.objects.all().delete()
    except:
        pass

    try:
        #CONNECT TO posgresql
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        con = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        con.set_session(readonly=False)
        cur = con.cursor()
        cur.execute("alter table \"Utmmetka_country\" alter column \"name\" type character varying(300);")
        cur.execute("alter table \"Utmmetka_city\" alter column \"name\" type character varying(300);")
        cur.execute("alter table \"Utmmetka_firstvar\" alter column \"utm_campaign\" type character varying(300);")
        cur.execute("alter table \"Utmmetka_firstvar\" alter column \"utm_term\" type character varying(300);")
        cur.execute("alter table \"Utmmetka_firstvar\" alter column \"utm_content\" type character varying(300);")
        cur.execute("alter table \"Utmmetka_firstvar\" alter column \"utmname\" type character varying(300);")
        cur.execute("alter table \"Utmmetka_urlname\" alter column \"name\" type character varying(300);")
        cur.execute("alter table \"Startpage_langing\" alter column \"land\" type character varying(300);")
        cur.execute("alter table \"Startpage_langing\" alter column \"success\" type character varying(300);")
        cur.execute("alter table \"Startpage_langing\" alter column \"complete\" type character varying(300);")

        j = 1
        p = 1
        with con:
            cur = con.cursor()
            global c
            for i in c:
                cur.execute("INSERT INTO  \"Utmmetka_country\" VALUES(" + str(j) + ", '" + str(i) + "')")
                global k
                for jj in k[i][1:]:
                    cur.execute(
                        "INSERT INTO  \"Utmmetka_city\" VALUES(" + str(p) + ", '" + str(jj[0]) + "', " + str(j) + ")")
                    p += 1
                j += 1
    except:
        # CONNECT TO  sql
        import sqlite3 as lite
        con = lite.connect('db.sqlite3')
        j = 1
        p = 1
        with con:
            cur = con.cursor()
            for (table_name,) in cur:
                print(table_name)
            for i in c:
                cur.execute("INSERT INTO  Utmmetka_country VALUES(" + str(j) + ", '" + str(i) + "')")
                for jj in k[i][1:]:
                    cur.execute(
                        "INSERT INTO  Utmmetka_city VALUES(" + str(p) + ", '" + str(jj[0]) + "', " + str(j) + ")")
                    p += 1
                j += 1



class PersonListView(ListView):
    model = Firstvar
    print(type(model))
    template_name = 'hr/person_list.html'
    context_object_name = 'people'
    insertinsql()


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'hr/person_form.html'
    success_url = reverse_lazy('person_changelist')


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})


def checkform(country, city):
    global k
    dataframe = pd.DataFrame(k[country][1:], columns=k[country][0])
    checkform = str(dataframe.loc[dataframe['Название'] == city, 'utm_source'].item()) + ' ' + str(
        dataframe.loc[dataframe['Название'] == city, 'utm_medium'].item()) + ' ' + str(
        dataframe.loc[dataframe['Название'] == city, 'utm_campaign'].item()) + ' ' + str(
        dataframe.loc[dataframe['Название'] == city, 'utm_term'].item()) + ' ' + str(
        dataframe.loc[dataframe['Название'] == city, 'utm_content'].item())
    countchekform = checkform.count('введите')
    return countchekform


def nameinsert(country, city):
    allinsert = []
    global k
    dataframe = pd.DataFrame(k[country][1:], columns=k[country][0])
    for i in [dataframe.loc[dataframe['Название'] == city, 'utm_source'].item(),
              dataframe.loc[dataframe['Название'] == city, 'utm_medium'].item(),
              dataframe.loc[dataframe['Название'] == city, 'utm_campaign'].item(),
              dataframe.loc[dataframe['Название'] == city, 'utm_term'].item(),
              dataframe.loc[dataframe['Название'] == city, 'utm_content'].item()]:
        if 'введите' in i:
            allinsert.append(i)
    return allinsert


def deleteNO(query, stopwords):
    querywords = query.split('&')
    resultwords = [word for word in querywords if word.lower() not in stopwords]
    result = '&'.join(resultwords)
    return result


def utmnamecreate(country, city, countvvod, utm_campaign, utm_term, utm_content):
    url = cyrtranslit.to_latin(str(Urlname.objects.last().name), 'ru').replace(" ", "")
    global k
    dataframe = pd.DataFrame(k[country][1:], columns=k[country][0])
    print(dataframe.loc[dataframe['Название'] == city, 'utm_source'])
    utmname = url + '?' + 'utm_source=' + str(
        dataframe.loc[dataframe['Название'] == city, 'utm_source'].item()) + '&utm_medium=' + str(
        dataframe.loc[dataframe['Название'] == city, 'utm_medium'].item()) + '&utm_campaign=' + str(
        dataframe.loc[dataframe['Название'] == city, 'utm_campaign'].item()) + '&utm_term=' + str(
        dataframe.loc[dataframe['Название'] == city, 'utm_term'].item()) + '&utm_content=' + str(
        dataframe.loc[dataframe['Название'] == city, 'utm_content'].item()) + '&'
    if countvvod == 1:
        find = re.findall(r'введите.*?[&]', utmname)
        newline = utmname.replace(find[0], utm_campaign + '&')
        itogfirst = deleteNO(newline[:-1], re.findall(r'[^&]*нет', newline[:-1]))
        itog = cyrtranslit.to_latin(itogfirst, 'ru').replace(" ", "")
        return itog

    elif countvvod == 2:
        find = re.findall(r'введите.*?[&]', utmname)
        newline = utmname.replace(find[0], utm_campaign + '&')
        newline1 = newline.replace(find[1], utm_term + '&')
        itogfirst = deleteNO(newline1[:-1], re.findall(r'[^&]*нет', newline1[:-1]))
        itog = cyrtranslit.to_latin(itogfirst, 'ru').replace(" ", "")
        return itog

    elif countvvod == 3:
        find = re.findall(r'введите.*?[&]', utmname)
        newline = utmname.replace(find[0], utm_campaign + '&')
        newline1 = newline.replace(find[1], utm_term + '&')
        newline2 = newline1.replace(find[2], utm_content + '&')
        itogfirst = deleteNO(newline2[:-1], re.findall(r'[^&]*нет', newline2[:-1]))
        itog = cyrtranslit.to_latin(itogfirst, 'ru').replace(" ", "")
        return itog
    else:
        itogfirst = deleteNO(utmname[:-1], re.findall(r'[^&]*нет', utmname[:-1]))
        itog = cyrtranslit.to_latin(itogfirst, 'ru').replace(" ", "")
        return itog


def index2(request):
    d = {}
    if (request.method == 'POST'):
        forminlist = PersonForm(request.POST)
        forminlist.save()
    person = Person.objects.last()
    a = checkform(str(Person.objects.last().country), str(Person.objects.last().city))
    b = nameinsert(str(Person.objects.last().country), str(Person.objects.last().city))
    if a == 1:
        form = FirstForm
        d['form'] = form
        d['nameinsertfirst'] = b[0]
    elif a == 2:
        form = SecondForm
        d['form'] = form
        d['nameinsertfirst'] = b[0]
        d['nameinsertsecond'] = b[1]
    elif a == 3:
        form = ThirdForm
        d['form'] = form
        d['nameinsertfirst'] = b[0]
        d['nameinsertsecond'] = b[1]
        d['nameinsertthird'] = b[2]
    else:
        utmname = utmnamecreate(str(Person.objects.last().country), str(Person.objects.last().city), a, None, None, None)
        encodeurl = urllib.parse.quote(utmname)
        fetcher = urllib2.urlopen('https://clck.ru/--?url=' + encodeurl)
        clickmename = fetcher.read().decode()
        Firstvar.objects.create(person=person, utmname=utmname, urlname=str(Urlname.objects.last().name),clickmename=clickmename)
        return redirect('/utmgenerator')
    
    return render(request, 'hr/pagenext.html', d)


def index3(request):
    if (request.method == 'POST'):
        person = Person.objects.last()
        a = checkform(str(Person.objects.last().country), str(Person.objects.last().city))
        if a == 1:
            utmname = utmnamecreate(str(Person.objects.last().country), str(Person.objects.last().city), a,request.POST['utm_campaign'], None, None)
            encodeurl = urllib.parse.quote(utmname)
            fetcher = urllib2.urlopen('https://clck.ru/--?url=' + encodeurl)
            clickmename = fetcher.read().decode()
            Firstvar.objects.create(utm_campaign=request.POST['utm_campaign'], person=person, utmname=utmname,urlname=str(Urlname.objects.last().name), clickmename=clickmename)
        elif a == 2:
            utmname = utmnamecreate(str(Person.objects.last().country), str(Person.objects.last().city), a,request.POST['utm_campaign'], request.POST['utm_term'], None)
            encodeurl = urllib.parse.quote(utmname)
            fetcher = urllib2.urlopen('https://clck.ru/--?url=' + encodeurl)
            clickmename = fetcher.read().decode()
            Firstvar.objects.create(utm_campaign=request.POST['utm_campaign'], utm_term=request.POST['utm_term'],person=person, utmname=utmname, urlname=str(Urlname.objects.last().name),clickmename=clickmename)
        elif a == 3:
            utmname = utmnamecreate(str(Person.objects.last().country), str(Person.objects.last().city), a,request.POST['utm_campaign'], request.POST['utm_term'], request.POST['utm_content'])
            encodeurl = urllib.parse.quote(utmname)
            fetcher = urllib2.urlopen('https://clck.ru/--?url=' + encodeurl)
            clickmename = fetcher.read().decode()
            Firstvar.objects.create(utm_campaign=request.POST['utm_campaign'], utm_term=request.POST['utm_term'],utm_content=request.POST['utm_content'], person=person, utmname=utmname,urlname=str(Urlname.objects.last().name), clickmename=clickmename)
    return redirect('/utmgenerator')


def inserturl(request):
    d = {}
    form = UrlForm()
    d['form'] = form

    return render(request, 'hr/urlname.html', d)


def inserturl2(request):
    if (request.method == 'POST'):
        form = UrlForm(request.POST)
        form.save()

    return redirect('/utmgenerator/hr/add/')


