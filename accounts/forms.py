from django import forms

from .models import Account,UserProfile

#creating forms using Django
class RegistrationForm(forms.ModelForm):

    #creating password field
    password = forms.CharField(widget=forms.PasswordInput(attrs={
    'placeholder':'Enter Password', #providing placeholder in html page
    'class':'form-control', #providing css class in html page
    }))
    #creating password field
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    class Meta:
        #Inheriting account class from models.py
        model = Account

        #fields that we need to work on
        #(username is not included as we will be generating it automatically from emailid)
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']


    def __init__(self, *args, **kwargs):
        '''Overriding the functionality of RegistrationForm to provide CSS class and placeholder to whole HTML form fields'''
        super(RegistrationForm,self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


    def clean(self):
        ''' Checking password and confirm_password are equal or not '''
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
            "Password does not match!"
            )



class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name','last_name','phone_number')

    def __init__(self, *args, **kwargs):
        '''Overriding the functionality of UserForm to provide CSS class and placeholder to whole HTML form fields'''
        super(UserForm,self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    #It gives a good file browse option
    profile_picture = forms.ImageField(required=False,error_messages = {'invalid':('Image files only')},widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')

    def __init__(self, *args, **kwargs):
        '''Overriding the functionality of UserProfileForm to provide CSS class and placeholder to whole HTML form fields'''
        super(UserProfileForm,self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
