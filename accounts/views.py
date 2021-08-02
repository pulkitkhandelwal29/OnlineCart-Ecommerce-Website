from django.shortcuts import render,redirect

from .forms import RegistrationForm

from .models import Account

from django.contrib import messages #django messages
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name'] #Accessing value from form using "cleaned_data"
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user( #calling the function 'create_user' from MyAccountManager in accounts (models)
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
            password = password,
            #we are not giving phone number as to create user we do not require it (according to models.py create_user function)
            )
            user.phone_number = phone_number
            user.save()
            messages.success(request,'Registration successful') #if everything is successful, show this message
            return redirect('register')

    else:
        form = RegistrationForm() #calling the class from forms.py file

    context={'form':form}
    return render(request,'accounts/register.html',context)

def login(request):
    return render(request,'accounts/login.html')

def logout(request):
    return render(request,'accounts/logout.html')
