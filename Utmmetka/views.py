from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Person, City,Country
from .forms import PersonForm,FirstForm
from .conecttosheets import Connection,UTMtable,PSP
from django.http import HttpResponseRedirect
import psycopg2
import os
import urllib.parse as urlparse
from django.shortcuts import redirect



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
    gs = Connection()
    gs.connect()
    utm = UTMtable(gs.service)
    utm.getSheets()
    #Connect to bd
    #con = lite.connect('postgresql-aerodynamic-82180')
    #con = psycopg2.connect(dbname='postgresql-aerodynamic-82180', user='razumovr',password='123456789qQ')
    
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
    print(con)
    con.set_session(readonly=False)
    cur = con.cursor()
    cur.execute("alter table \"Utmmetka_country\" alter column \"name\" type character varying(500);")
    cur.execute("alter table \"Utmmetka_city\" alter column \"name\" type character varying(500);")

    #for table in cur.fetchall():
    #    print(table)
    
    j=1
    p = 1
    try:
         with con:
             cur = con.cursor()
             for (table_name,) in cur:
                 print(table_name)
             for i in utm.tables.keys():
                 cur.execute("INSERT INTO  Utmmetka_country VALUES("+str(j)+", '"+str(i)+"')")
                 for jj in utm.tables[i][1:]:
                     cur.execute("INSERT INTO  Utmmetka_city VALUES(" + str(p) + ", '" + str(jj[0]) + "', " +str(j) +")")
                     p+=1
                 j+=1
     except:
         pass
 

class PersonListView(ListView):
    model = Person
    template_name = 'hr/person_list.html'
    context_object_name = 'people'
    insertinsql()
    print("PROVERKA")


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
    print("HEYYYYY")
    print(request.POST)
    print(country_id)
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'hr/city_dropdown_list_options.html', {'cities': cities})



def index2(request):

    d={}
    form=FirstForm
    d['form']=form
    if(request.method=='POST'):
        forminlist=PersonForm(request.POST)
        forminlist.save()
    print(request.POST['country'])
    return render(request,'hr/pagenext.html',d)


def index3(request):
    if(request.method=='POST'):
        person = Person.objects.last()
        Firstvar.objects.create(name=request.POST['name'], person=person,utmname='?utm_source=email&utm_medium=segment&utm_campaign=fin&utm_term=123&utm_content=1488')
    return redirect('https://deliveryclub.herokuapp.com/utmgenerator')
