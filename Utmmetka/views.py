from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Person, City,Country,Firstvar
from .forms import PersonForm,FirstForm,SecondForm,ThirdForm
from .conecttosheets import Connection,UTMtable,PSP
import urllib.parse as urlparse
from django.shortcuts import redirect

import pandas as pd

gs = Connection()
gs.connect()
utm = UTMtable(gs.service)
b=utm.getSheets()
c=utm.tables.keys()
k=utm.tables

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
    '''cur.execute("alter table \"Utmmetka_country\" alter column \"name\" type character varying(500);")
    cur.execute("alter table \"Utmmetka_city\" alter column \"name\" type character varying(500);")
    with con:
        cur = con.cursor()
        global c
        for i in c:
            cur.execute("INSERT INTO  \"Utmmetka_country\" VALUES("+str(j)+", '"+str(i)+"')")
            global k
            for jj in k[i][1:]:
                cur.execute("INSERT INTO  \"Utmmetka_city\" VALUES(" + str(p) + ", '" + str(jj[0]) + "', " +str(j) +")")
                p+=1
            j+=1'''



class PersonListView(ListView):
    model =Firstvar
    print(type(model))
    template_name = 'hr/person_list.html'
    context_object_name = 'people'
    insertinsql()


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'hr/person_form.html'
    success_url = reverse_lazy('person_changelist')



class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')



def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})




def checkform(country,city):
    global k
    dataframe = pd.DataFrame(k[country][1:], columns=k[country][0])
    checkform = str(dataframe.loc[dataframe['Название'] == city, 'utm_campaign']) + ' ' + str(dataframe.loc[dataframe['Название'] == city, 'utm_term']) + ' ' + str(dataframe.loc[dataframe['Название'] == city, 'utm_content'])
    countchekform = checkform.count('введите')
    return countchekform





def index2(request):
    d={}
    if(request.method=='POST'):
        forminlist=PersonForm(request.POST)
        forminlist.save()
    person = Person.objects.last()
    a=checkform(str(Person.objects.last().country),str(Person.objects.last().city))
    if a==1:
        form = FirstForm
        d['form'] = form
    elif a==2:
        form = SecondForm
        d['form'] = form
    elif a==3:
        form = ThirdForm
        d['form'] = form
    else:
        Firstvar.objects.create(person=person,utmname='?utm_source=email&utm_medium=segment&utm_campaign=fin&utm_term=123&utm_content=1488')
        return redirect('https://deliveryclub.herokuapp.com/utmgenerator')
    return render(request,'hr/pagenext.html',d)


def index3(request):
    if(request.method=='POST'):
        person = Person.objects.last()
        a = checkform(str(Person.objects.last().country), str(Person.objects.last().city))
        if a == 1:
            Firstvar.objects.create(utm_campaign=request.POST['utm_campaign'],person=person,utmname='?utm_source=email&utm_medium=segment&utm_campaign=fin&utm_term=123&utm_content=1488')
        elif a == 2:
            Firstvar.objects.create(utm_campaign=request.POST['utm_campaign'],utm_term=request.POST['utm_term'],person=person,utmname='?utm_source=email&utm_medium=segment&utm_campaign=fin&utm_term=123&utm_content=1488')
        elif a == 3:
            Firstvar.objects.create(utm_campaign=request.POST['utm_campaign'],utm_term=request.POST['utm_term'],utm_content=request.POST['utm_content'], person=person,utmname='?utm_source=email&utm_medium=segment&utm_campaign=fin&utm_term=123&utm_content=1488')
    return redirect('https://deliveryclub.herokuapp.com/utmgenerator')



