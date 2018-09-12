#https://docs.djangoproject.com/en/2.1/topics/forms/
# https://tutorial.djangogirls.org/es/django_forms/
from django import forms
from .models import Movimiento 


class FilterForm(forms.ModelForm):
    class Meta:
        model =  Movimiento
        fields=  ('producto', 'tipo',  'actividad')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False 
 