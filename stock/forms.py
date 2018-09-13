#https://docs.djangoproject.com/en/2.1/topics/forms/
# https://tutorial.djangogirls.org/es/django_forms/
from django import forms
from .models import Movimiento 


class FilterForm(forms.ModelForm):
    orden = forms.ChoiceField(choices=[
        ('producto', 'Producto (asc)'), 
        ('-producto', 'Producto (desc)'),
        ('tipo', 'Tipo (asc)'), 
        ('-tipo', 'Tipo (desc)'),
         ('actividad', 'Actividad (asc)'), 
        ('-actividad', 'Actividad (desc)')       
    ])
    class Meta:
        model =  Movimiento
        fields= ('producto', 'tipo',  'actividad', 'orden')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False 
 