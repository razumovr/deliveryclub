from .models import Langing
from django.forms import ModelForm,TextInput

class LangingForm(ModelForm):
    class Meta:
        model=Langing
        fields=['land','success','start','end','complete','heshteg',]
        widgets={'land':TextInput(attrs={'class': '',
                                         'name':'компания'
                                         }
                                  ),
                 'success': TextInput(attrs={'class': '',
                                          'name': 'компания'
                                          }),
                 'start': TextInput(attrs={'class': '',
                                          'name': 'компания'
                                          }
                                   ),
                 'end': TextInput(attrs={'class': '',
                                             'name': 'компания'
                                             }),
                 'complete': TextInput(attrs={'class': '',
                                          'name': 'компания'
                                          }
                                   ),
                 'heshteg': TextInput(attrs={'class': '',
                                             'name': 'компания'
                                             })
                 }
