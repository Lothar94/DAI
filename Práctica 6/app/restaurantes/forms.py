# restaurantes/forms.py

from django import forms
from django.core.exceptions import ValidationError

def validate_postal_code(value):
    if value < 10000 or value > 99999:
        raise ValidationError('%s no parece ser un código postal' % value)

class RestaurantForm(forms.Form):
    name = forms.CharField(
        label='Nombre',
        max_length=60,
        strip=True,
        widget=forms.TextInput(
            attrs={ 'size':30,
                    'placeholder':'Nombre',
        })
    )

    cuisine = forms.CharField(
        label='Tipo',
        max_length=80,
        required=False,
        widget=forms.TextInput(
            attrs={ 'size':30,
                    'placeholder':'Mejicana',
        })
    )

    zipcode = forms.IntegerField(
        label='Código Postal',
        validators=[validate_postal_code],
        widget=forms.TextInput(
            attrs={ 'size':30,
        })
    )
