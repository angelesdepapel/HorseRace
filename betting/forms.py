from django import forms

class BetForm(forms.Form):
    name = forms.CharField(max_length = 80)
    rut = forms.CharField(max_length = 12)
    amount = forms.PositiveIntegerField(min_value = 1)