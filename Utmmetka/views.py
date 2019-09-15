from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Person, City,Country
from .forms import PersonForm,FirstForm
from .conecttosheets import Connection,UTMtable,PSP
from django.http import HttpResponseRedirect
import psycopg2
import os


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
    DATABASE_URL = os.environ['DATABASE_URL']
    con = psycopg2.connect(DATABASE_URL, sslmode='require')
    j=1
    p = 1
    with con:
        cur = con.cursor()
        for i in utm.tables.keys():
            cur.execute("INSERT INTO  Utmmetka_country VALUES("+str(j)+", '"+str(i)+"')")

            for jj in utm.tables[i][1:]:
                cur.execute("INSERT INTO  Utmmetka_city VALUES(" + str(p) + ", '" + str(jj[0]) + "', " +str(j) +")")
                p+=1
            j+=1


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
    '''if(request.method=='POST'):
        print(request.POST)
        forminlist=FirstForm(request.POST)
        forminlist.save()'''
    '''print('!'*100)
    print(request.POST)
    print('!'*100)'''
    print('HEEEEEEy')
    print(d)
    print(request.POST['country'])
    return render(request,'hr/pagenext.html',d)


def index3(request):
    print("ZAHHHHHOD"*20)
    if(request.method=='POST'):
        forminlist=FirstForm(request.POST)
        forminlist.save()
    return render(request, 'hr/person_list.html')
    #return render(request,a.success_url)
