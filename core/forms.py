from django.forms import ModelForm
from django import forms
from .models import DireccionEntrega, productos

class CheckoutForm(forms.Form):
    calle = forms.CharField(required=True)
    numeroExterior = forms.IntegerField(required=True)
    numeroInterior = forms.IntegerField(required=False)
    colonia = forms.CharField(required=True)
    rfc = forms.CharField(required=True)
    telefono = forms.CharField(required=True)
    codigoPostal = forms.IntegerField(required=True)

class addToCart(forms.Form):
    Cantidad =  forms.IntegerField(required=True)

class ProductEditForm(ModelForm):
    class Meta:
        model = productos
        fields = ['titulo', 'descripcion', 'image', 'disponible']
