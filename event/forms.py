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
            'profession',
            'gender',
            'blood_group',
            'spouse_name',
            'driver_coming',
            'participant_image',
            'spouse_image',
            'transaction_id',
            'amount',
            'transport',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profession': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'spouse_name': forms.TextInput(attrs={'class': 'form-control'}),
            'driver_coming': forms.Select(attrs={'class': 'form-control'}),
            'participant_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'spouse_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'transport': forms.Select(attrs={'class': 'form-control'}),
        }
