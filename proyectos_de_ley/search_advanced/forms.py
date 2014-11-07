from django import forms
from django.core.exceptions import ValidationError

from pdl.models import Proyecto


class SearchAdvancedForm(forms.Form):
    date_from = forms.DateField(
        label="Fecha inicio",
        required=False,
    )
    date_to = forms.DateField(
        label="Fecha fin",
        required=False,
    )

