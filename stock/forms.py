#https://docs.djangoproject.com/en/2.1/topics/forms/
# https://tutorial.djangogirls.org/es/django_forms/
from django import forms
from .models import Movimiento, Lote, Campaña, Cultivo
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class FilterForm(forms.ModelForm):
    actividad__campaña = forms.ModelChoiceField(label="Campaña",
                                                empty_label="Elegir campaña",
                                                queryset=Campaña.objects.all())
    actividad__campaña__lote = forms.ModelChoiceField(label="Lote",
                                                      empty_label="Elegir Lote",
                                                      queryset=Lote.objects.all())
    actividad__campaña__cultivo = forms.ModelChoiceField(label="Cultivo",
                                                         empty_label="Elegir cultivo",
                                                         queryset=Cultivo.objects.all())

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
        fields = ('producto', 'tipo',  'actividad', 'actividad__campaña__lote',
        'actividad__campaña', 'actividad__campaña__cultivo',
        'tipo_comp', 'letra_comp','pto_venta','nro_comp')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-form'
        self.helper.form_method = 'get'

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-form-label-sm'
        self.helper.field_class = 'col'

        self.helper.layout = Layout(
            Field(*self.fields, css_class='custom-select custom-select-sm',
            onchange='document.forms["id-form"].submit();')
        )

        self.fields['producto'].empty_label = "Elegir producto"
        self.fields['tipo'].empty_label = "Elegir tipo"
        self.fields['actividad'].empty_label = "Elegir actividad"
        self.fields['tipo_comp'].empty_label = "Elegir Tipo de comprobante "
        self.fields['letra_comp'].empty_label = "Elegir Letra"

        # self.helper.add_input(Submit('submit-button', 'Filtrar'))

        self.helper.add_input(Submit('submit-button', 'Filtrar', css_class='btn btn-primary btn-shadow btn-gradient'))

        #self.tipo_comp(default)  ## resetea valor para que no aplique filtro no deseado.
        #self.letra(default)  ## resetea valor para que no aplique filtro no deseado.

        for key in self.fields:
            self.fields[key].required = False
        self.fields['tipo_comp'].choices = [('', '---')] + Movimiento.OPC_TC
        self.fields['tipo_comp'].required = False
        self.fields['letra_comp'].choices = [('', '---')] + Movimiento.OPC_LETRA
        self.fields['letra_comp'].required = False


class MovimientoModelForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = [
            'producto', 'tipo', 'cantidad', 'descripcion',
            'fecha', 'es_inicial', 'precio_peso',
            'precio_dolar', 'tipo_comp', 'letra_comp', 'pto_venta',
            'nro_comp'
        ]
