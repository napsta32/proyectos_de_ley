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
    comision = forms.CharField(
        label='Comisión',
        required=False,
    )
