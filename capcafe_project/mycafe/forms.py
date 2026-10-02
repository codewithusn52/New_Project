from .models import MenuItem
from django import forms
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['category', 'name', 'description', 'price', 'is_available']
        widgets={
            'category': forms.Select(attrs={'class':'forms=select'}),
            'name': forms.TextInput(attrs={'class':'form=control','placeholder':'e.g, Espresso'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief item description...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

        }
