from functools import partial

from django import forms
from django.core.exceptions import ValidationError

from pdl.models import Proyecto


DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class SearchAdvancedForm(forms.Form):
    date_from = forms.DateField(
        widget=DateInput(),
        label="Fecha inicio",
        required=False,
    )
    date_to = forms.DateField(
        widget=DateInput(),
        label="Fecha fin",
        required=False,
    )

