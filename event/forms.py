# forms.py

from django import forms
from .models import Participant

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = [
            'name',
            'contact_number',
            'email',
            'district',
            'school_name',
            'gender',
            'profession',
            'blood_group',
            'participant_image',
            'spouse_name',
            'spouse_image',
            'driver_coming',
            'transaction_id',
            'paid_at',
            'amount',
            'transport',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control' }),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'profession': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'participant_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'spouse_name': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'spouse_image': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required': False}),
            'driver_coming': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'paid_at':forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'transport': forms.Select(attrs={'class': 'form-control'}),
        }
