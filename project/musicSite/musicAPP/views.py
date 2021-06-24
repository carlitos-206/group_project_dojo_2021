from django.shortcuts import render, HttpResponse, redirect
from .models import Users
from django.contrib import messages
import bcrypt

#Everyone make sure to write in the given space this will make it easier to debug

#----------------Carlos Views-----------
def index(request):
    return render(request, 'index.html')
def register(request):
    if request.method=="POST":
        errors = Users.objects.user_validation(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)      
            return redirect('/')
        pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user=Users.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            gender=request.POST['gender'],
            username=request.POST['username'],
            password=pw_hash,
        )
        request.session['user_id']=new_user.id
        return redirect('/dashboard')
def terms(request):
    return render(request, 'terms.html')
def sign_in(request):
    if request.method=="GET":
        return redirect('/')
    if request.method=="POST":
        if not Users.objects.login_validation(request.POST['password'], request.POST['username']):
            messages.error(request, "Invalid info")
            return redirect('/')
        this_user = Users.objects.filter(username=request.POST['username'])
        request.session['user_id'] = this_user[0].id
    return redirect("/dashboard")

def logout(request):
    request.session.flush()
    return redirect('/goodbye')
def farewell(request):
    return render(request, 'goodbye.html')

def dashboard(request):
    if 'user_id' in request.session:
        this_user=Users.objects.filter(id=request.session['user_id'])
        newest_party=Party.objects.filter(host=this_user[0])
        context = {
        'user': this_user[0],
        # need second db to contine @gustavo
    }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

#-------------END------------------------------------



#------------JAIME VIEWS----------------------

#-------------END------------------------------




#-----------CONNOR VIEWS------------------------

#--------------END--------------------------



#-------------GUSTAVO VIEWS---------------------

#---------------END--------------------------
