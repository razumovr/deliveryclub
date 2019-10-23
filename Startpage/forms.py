from .models import Langing
from django.forms import ModelForm,TextInput

class LangingForm(ModelForm):
    class Meta:
        model=Langing
        fields=['land','success','start','end','complete']
        widgets={'land':TextInput(attrs={'class': 'form-input',
                                         'name':'компания'
                                         }
                                  ),
                 'success': TextInput(attrs={'class': 'form-input',
                                          'name': 'компания'
                                          }),
                 'start': TextInput(attrs={'class': 'form-input',
                                          'name': 'компания'
                                          }
                                   ),
                 'end': TextInput(attrs={'class': 'form-input',
                                             'name': 'компания'
                                             }),
                 'complete': TextInput(attrs={'class': 'form-input',
                                          'name': 'компания'
                                          }
                                   ),

                 }
