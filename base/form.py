from django import forms
from .models import Account,Order

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Account
        fields = ['first_name','last_name','username','email','phone_number','password']


    def clean(self):
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )
        

    def __init__(self,*args, **kwargs):
        super(RegistrationForm , self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-lg'



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name','email','phone','address_line_1','address_line_2','country','state','city']
