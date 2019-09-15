from django import forms
#from django.forms import ModelForm,TextInput

from .models import Person, City,Firstvar

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')



class FirstForm(forms.ModelForm):
    class Meta:
        model=Firstvar
        fields=['name']


        widgets={'name':forms.TextInput(attrs={'class': 't-input js-tilda-rule   t-input_pvis',
                                         'name':'компания',
                                         'placeholder':"Введите лендинг",
                                         'data - tilda - req' : "1",
                                         'style' : "color:#000000; border:1px solid #000000;  ",
                                         }
                                  ),
                 }
