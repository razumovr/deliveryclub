from django.shortcuts import render
from .models import Langing
from .forms import LangingForm
from .project import main


'''def index2(request):
    d=main()
    Langing.objects.all().delete()

    return render(request,'mainpage/pagenext.html',d)'''


def index(request):
    d={}

    form=LangingForm()

    d['form']=form

    return render(request,'mainpage/index.html',d)


def index2(request):
    print('!'*100)
    print(request.POST)
    print('!'*100)

    if(request.method=='POST'):

        form=LangingForm(request.POST)
        form.save()
        print("SAVE IS OK")



    d=main()
    Langing.objects.all().delete()

    return render(request,'mainpage/page2.html',d)