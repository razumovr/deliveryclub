from .models import Langing
from django.forms import ModelForm,TextInput

class LangingForm(ModelForm):
    class Meta:
        model=Langing
        fields=['land','success','start','end','complete','heshteg',]


        widgets={'land':TextInput(attrs={'class': '',
                                         'name':'компания',
                                         'placeholder':"Введите лендинг"
                                         }
                                  ),
                 'success': TextInput(attrs={'class': '',
                                          'name': 'компания',
                                          'placeholder': "Введите success"
                                          }),
                 'start': TextInput(attrs={'class': '',
                                          'name': 'компания',
                                          'placeholder': "Введите начальную дату"
                                          }
                                   ),
                 'end': TextInput(attrs={'class': '',
                                             'name': 'компания',
                                             'placeholder': "Введите конечную дату"
                                             }),
                 'complete': TextInput(attrs={'class': '',
                                          'name': 'компания',
                                          'placeholder': "Введите completesheet"
                                          }
                                   ),
                 'heshteg': TextInput(attrs={'class': '',
                                             'name': 'компания',
                                             'placeholder': "Введите хештег"
                                             })
                 }
