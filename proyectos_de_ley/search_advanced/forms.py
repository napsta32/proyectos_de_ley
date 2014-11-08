from functools import partial

from django import forms
from django.core.exceptions import ValidationError

from pdl.models import Proyecto


DateInput1 = partial(forms.DateInput, {'class': 'datepicker',
                                       'placeholder': 'Fecha inicio'})
DateInput2 = partial(forms.DateInput, {'class': 'datepicker',
                                       'placeholder': 'Fecha fin'})


class SearchAdvancedForm(forms.Form):
    date_from = forms.DateField(
        widget=DateInput1(),
        label="Fecha inicio",
        required=False,
    )
    date_to = forms.DateField(
        widget=DateInput2(),
        label="Fecha fin",
        required=False,
    )

