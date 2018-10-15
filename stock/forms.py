#https://docs.djangoproject.com/en/2.1/topics/forms/
# https://tutorial.djangogirls.org/es/django_forms/
from django import forms
from .models import Movimiento, Lote, Campaña, Cultivo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


class FilterForm(forms.ModelForm):
    actividad__campaña__lote = forms.ModelChoiceField(label="Lote", queryset=Lote.objects.all())
    actividad__campaña = forms.ModelChoiceField(label="Campaña", queryset=Campaña.objects.all())
    actividad__campaña__cultivo = forms.ModelChoiceField(label="Cultivo", queryset=Cultivo.objects.all())

    class Meta:
        model =  Movimiento
        fields=  ('producto', 'tipo',  'actividad', 'actividad__campaña__lote',
        'actividad__campaña', 'actividad__campaña__cultivo')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'form'
        self.helper.form_class = ''
        self.helper.form_method = 'get'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            Field(#'producto',
            '{% for field in fields%}',
            onchange = 'this.forms.submit();',)
        )

        self.helper.add_input(Submit('submit', 'Filtrar'))

        for key in self.fields:
            self.fields[key].required = False
