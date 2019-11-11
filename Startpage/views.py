from django.shortcuts import render
from .models import Langing
from .forms import LangingForm
from .project import main,main_for_new_funnel


def indexstartpage(request):
    return render(request,'start.html')

def choose(request):
    return render(request,'choose.html')


def index(request):
    d={}
    form=LangingForm()
    d['form']=form

    return render(request,'mainpage/index.html',d)


def index_for_new_funnel(request):
    d={}
    form=LangingForm()
    d['form']=form

    return render(request,'mainpage/index_for_new_funnel.html',d)


def index2(request):
    if(request.method=='POST'):

        form=LangingForm(request.POST)
        form.save()

    d=main()
    Langing.objects.all().delete()

    return render(request,'mainpage/page2.html',d)

def index2_new(request):
    if(request.method=='POST'):

        form=LangingForm(request.POST)
        form.save()

    d=main_for_new_funnel()
    Langing.objects.all().delete()

    return render(request,'mainpage/page2_for_new.html',d)


def index3(request):
    return render(request,'mainpage/styles/style.css')
