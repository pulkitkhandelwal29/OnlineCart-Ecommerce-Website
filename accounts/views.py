from django.shortcuts import render,redirect

from .forms import RegistrationForm

from .models import Account

from django.contrib import messages #django messages

from django.contrib import auth

from django.contrib.auth.decorators import login_required

#verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.http import HttpResponse
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

            #USER Activation
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/account_verification_email.html',{ #Write email body in HTML
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), #encoding the user uid (later we will decode)
                'token':default_token_generator.make_token(user), #creates token
                })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send() #send email

            # messages.success(request,'Registration successful') #if everything is successful, show this message
            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form = RegistrationForm() #calling the class from forms.py file

    context={'form':form}
    return render(request,'accounts/register.html',context)



def login(request):
    if request.method == "POST":
        email = request.POST['email'] #accesing email from form
        password = request.POST['password']

        user = auth.authenticate(request,email=email, password=password)

        if user is not None:
            auth.login(request,user) #If user exists, login with this user
            messages.success(request,"You are now logged in.") #(We will be doing this is dashboard)
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')

    return render(request,'accounts/login.html')


@login_required(login_url = 'login') #if not logged in, redirect to url 'login'
def logout(request):
    auth.logout(request)
    messages.success(request,"You are logged out.")
    return redirect('login')





def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations! Your account is activated.')
        return redirect('login')

    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')



@login_required(login_url = 'login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():  #Check if the email exists or not
            user = Account.objects.get(email__exact=email)

            #Reset Password email
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string('accounts/reset_password_email.html',{ #Write email body in HTML
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), #encoding the user uid (later we will decode)
                'token':default_token_generator.make_token(user), #creates token
                })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send() #send email

            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('login')

        else:
            messages.error(request,'Account does not exist!')
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')



def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token): #checking token (to check secure request)
        request.session['uid'] = uid #uid saved in session to reset password below
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')

    else:
        messages.error(request,'This link has been expired')
        return redirect('login')



def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password) #setting the password
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('login')

        else:
            messages.error(request,'Password do not match!')
            return redirect('resetPassword')

    else:
        return render(request,'accounts/resetPassword.html')
