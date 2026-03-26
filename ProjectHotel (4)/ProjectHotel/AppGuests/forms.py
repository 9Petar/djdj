from django import forms
from AppStaff.models import Room, Guest
from .models import Booking
from datetime import date

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'id_front', 'id_back']

    first_name = forms.CharField(max_length=100, required=True, 
        widget = forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'form-control'
            }
    ))
    last_name = forms.CharField(max_length=100, required=True,
        widget = forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'form-control'
            }
    ))
    email = forms.EmailField(required=True,
        widget = forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            }
    ))
    phone_number = forms.CharField(max_length=15, required=True,
        widget = forms.TextInput(
            attrs={
                'placeholder': 'Phone Number',
                'class': 'form-control'
            }
    ))
    id_front = forms.ImageField(required=True,
        widget = forms.ClearableFileInput(
            attrs={
                'class': 'form-control'
            }
    ))
    id_back = forms.ImageField(required=True,
        widget = forms.ClearableFileInput(
            attrs={
                'class': 'form-control'
            }
    ))


    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'number_of_guests']

    room_type = forms.ChoiceField(choices=Room.ROOM_TYPE_CHOICES, required=True, 
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
    ))
    check_in = forms.DateField(required=True, 
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
    ))
    check_out = forms.DateField(required=True, 
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
    ))
    number_of_guests = forms.IntegerField(min_value=1, max_value=10, required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control'
            }
    ))

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_in < date.today():
             self.add_error('check_in', "Datum dolaska ne može biti u prošlosti.")
        
        if check_in and check_out and check_out <= check_in:
            self.add_error('check_out', "Datum odlaska mora biti nakon datuma dolaska.")
            
        return cleaned_data

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Your Name',
                'class': 'form-control'
            }
    ))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Your Email',
                'class': 'form-control'
            }
    ))
    subject = forms.CharField(max_length=200, required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Subject',
                'class': 'form-control'
            }
    ))
    message = forms.CharField(required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Your Message',
                'class': 'form-control',
                'rows': 5
            }
    ))