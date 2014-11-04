from django import forms

class SearchAdvancedForm(forms.Form):
    date_start = forms.DateField()
    date_end = forms.DateField()