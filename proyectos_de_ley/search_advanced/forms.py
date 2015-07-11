from functools import partial

from django import forms


DateInput1 = partial(forms.DateInput, {'class': 'datepicker form-control',
                                       'placeholder': 'Fecha inicio'})
DateInput2 = partial(forms.DateInput, {'class': 'datepicker form-control',
                                       'placeholder': 'Fecha fin'})


class SearchAdvancedForm(forms.Form):
    date_from = forms.DateField(
        widget=DateInput1(),
        label="Fecha inicio",
        required=False,
        error_messages={'invalid': 'Ingrese fecha válida'},
    )
    date_to = forms.DateField(
        widget=DateInput2(),
        label="Fecha fin",
        required=False,
        error_messages={'invalid': 'Ingrese fecha válida'},
    )
    comision = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Comisión',
        required=False,
        choices=[
            ('---', '---'),
            ('Agraria', 'Agraria'),
            ('Ciencia', 'Ciencia'),
            ('Comercio Exterior', 'Comercio Exterior'),
            ('Constitución', 'Constitución'),
            ('Cultura', 'Cultura'),
            ('Defensa del Consumidor', 'Defensa del Consumidor'),
            ('Defensa Nacional', 'Defensa Nacional'),
            ('Descentralización', 'Descentralización'),
            ('Economía', 'Economía'),
            ('Educación', 'Educación'),
            ('Energía', 'Energía'),
            ('Fiscalización', 'Fiscalización'),
            ('Inclusión Social', 'Inclusión Social'),
            ('Inteligencia', 'Inteligencia'),
            ('Justicia', 'Justicia'),
            ('Mujer', 'Mujer'),
            ('Presupuesto', 'Presupuesto'),
            ('Producción Micro', 'Producción Micro'),
            ('Pueblos Andinos', 'Pueblos Andinos'),
            ('Relaciones Exteriores', 'Relaciones Exteriores'),
            ('Salud', 'Salud'),
            ('Trabajo', 'Trabajo'),
            ('Transportes', 'Transportes'),
            ('Vivienda', 'Vivienda'),
        ]
    )
    dispensados_2da_votacion = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Dispensados 2da votación',
        required=False,
        choices=[
            ('---', '---'),
            ('total', 'total'),
        ]
    )
