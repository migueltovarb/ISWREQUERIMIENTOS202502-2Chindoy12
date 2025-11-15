from django import forms # type: ignore
from .models import vehiculo

class vehiculoForm(forms.ModelForm):
    
    class Meta:
        model = vehiculo
        fields = [
            'placa',
            'marca',
            'modelo',
            'color'
        ]

        labels = {
            'placa': 'Placa',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'color': 'Color'
        }

        widgets = {
            'placa': forms.TextInput(attrs={'class':'form-control'}),
            'marca': forms.TextInput(attrs={'class':'form-control'}),
            'modelo': forms.NumberInput(attrs={'class':'form-control'}),
            'color': forms.Select(attrs={'class':'form-control'}),
        }
