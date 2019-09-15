from .models import Langing
from django.forms import ModelForm,TextInput

class LangingForm(ModelForm):
    class Meta:
        model=Langing
        fields=['land','success','start','end','complete','heshteg',]


        widgets={'land':TextInput(attrs={'class': 't-input js-tilda-rule   t-input_pvis',
                                         'name':'компания',
                                         'placeholder':"Введите лендинг",
                                         'data - tilda - req' : "1",
                                         'style' : "color:#000000; border:1px solid #000000;  ",
                                         }
                                  ),
                 'success': TextInput(attrs={'class': 't-input js-tilda-rule   t-input_pvis',
                                          'name': 'компания',
                                          'placeholder': "Введите success",
                                          'data - tilda - req': "1",
                                          'style': "color:#000000; border:1px solid #000000;  ",
                                          }),
                 'start': TextInput(attrs={'class': 't-input js-tilda-rule   t-input_pvis',
                                          'name': 'компания',
                                          'placeholder': "Введите начальную дату",
                                          'data - tilda - req': "1",
                                          'style': "color:#000000; border:1px solid #000000;  ",
                                          }
                                   ),
                 'end': TextInput(attrs={'class': 't-input js-tilda-rule   t-input_pvis',
                                             'name': 'компания',
                                             'placeholder': "Введите конечную дату",
                                             'data - tilda - req': "1",
                                             'style': "color:#000000; border:1px solid #000000;  ",
                                             }),
                 'complete': TextInput(attrs={'class': 't-input js-tilda-rule   t-input_pvis',
                                          'name': 'компания',
                                          'placeholder': "Введите completesheet",
                                          'data - tilda - req': "1",
                                          'style': "color:#000000; border:1px solid #000000;  ",
                                          }
                                   ),
                 'heshteg': TextInput(attrs={'class': 't-input js-tilda-rule   t-input_pvis',
                                             'name': 'компания',
                                             'placeholder': "Введите хештег",
                                             'data - tilda - req': "1",
                                             'style': "color:#000000; border:1px solid #000000;  ",
                                             }),
                 }
