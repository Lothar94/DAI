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

    street = forms.CharField(
        label='Calle',
        max_length=60,
        strip=True,
        widget=forms.TextInput(
            attrs={ 'size':30,
                    'placeholder':'Calle',
        })
    )

    building = forms.IntegerField(
        label='Número'
    )

    borough = forms.CharField(
        label='Barrio',
        max_length=60,
        strip=True,
        widget=forms.TextInput(
            attrs={ 'size':30,
                    'placeholder':'Barrio',
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
        validators=[validate_postal_code]
    )

class RestaurantEditForm(forms.Form):
    restaurant_id = forms.IntegerField(
        label='Id',
        widget=forms.TextInput(
            attrs={ 'size': 30,
                    'id': 'restaurant_id',
                    'placeholder':'Id',
        })
    )

    name = forms.CharField(
        label='Nombre',
        max_length=60,
        strip=True,
        widget=forms.TextInput(
            attrs={ 'size':30,
                    'placeholder':'Nombre',
        })
    )

    street = forms.CharField(
        label='Calle',
        max_length=60,
        strip=True,
        widget=forms.TextInput(
            attrs={ 'size':30,
                    'placeholder':'Calle',
        })
    )

    building = forms.IntegerField(
        label='Número'
    )

    borough = forms.CharField(
        label='Barrio',
        max_length=60,
        strip=True,
        widget=forms.TextInput(
            attrs={ 'size':30,
                    'placeholder':'Barrio',
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
        validators=[validate_postal_code]
    )

class RestaurantFindForm(forms.Form):
    CHOICES = (('Cuisine', 'Cuisine'),
                ('Borough', 'Borough'),
                ('Name', 'Name'),
                ('Zip', 'Zip'),)
    field = forms.ChoiceField(choices=CHOICES)

    borough = forms.CharField(
        label='Barrio',
        max_length=60,
        strip=True,
        widget=forms.TextInput(
            attrs={ 'size':30,
                    'placeholder':'Barrio',
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
        validators=[validate_postal_code]
    )

    name = forms.CharField(
        label='Nombre',
        max_length=60,
        strip=True,
        widget=forms.TextInput(
            attrs={ 'size':30,
                    'placeholder':'Nombre',
        })
    )
