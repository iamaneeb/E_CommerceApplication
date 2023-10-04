from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Account
        fields = ['first_name','last_name','username','email','phone_number','password']

    def __init__(self,*args, **kwargs):
        super(RegistrationForm , self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'