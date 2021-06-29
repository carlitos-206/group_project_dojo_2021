from django.shortcuts import render, HttpResponse, redirect
from .models import Users, Group
from django.contrib import messages
import bcrypt
from .models import *

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
        context = {
        'user': this_user[0],
        # need second db to contine @gustavo
    }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('/')

#-------------END------------------------------------



#------------JAIME VIEWS----------------------
#def myGroups(request, name):


# if not 'user_id' in request.session:
#   return redirect("/")
#       context = {
#            "x": myGroups.objects.all(),
#            "user": User.objects.get(id=request.session['user_id']),
#    }
#    return render(request, "myGroups.html", context)


#def allGroups(request, name):
#    if 'user_id' in request.session:
##        this_user=Users.objects.filter(id=request.session['user_id'])
 #       context = {
 #       'user': this_user[0],
 #       'allGroups': Group.objects.all(),
 #   }
 #       return render(request, 'allGroups.html', context)
 #   else:
 #       return redirect('/')




def myGroups(request):
    if not 'user_id' in request.session:
        return redirect("/")

    user = Users.objects.get(id=request.session['user_id'])
    x = Group.objects.filter(owner=user.id)

    context = {
            "x": x,
            "user": user,
    }
    
    return render(request, "myGroups.html", context)

#def myGroups_delete(request, id):  #applies when hitting edit button on the main page
   # if not 'user_id' in request.session:
  #      return redirect("/")

  #  user = Users.objects.get(id=request.session['user_id'])
   # request.session['user_id'] = user.id
 #   if user.id == 'user_id':
 #       desc = Group.objects.get(id=id)
  #      desc.delete()
  #  return redirect("/myGroups")


def myGroups_delete(request, group_id):
    owner = request.session['user_id']
    if Group.objects.filter(id=group_id, owner=owner):
        myGroup=Group.objects.get(id=group_id)
        myGroup.delete()
        return redirect('/myGroups')
    else:
        messages.error(request, "Only host can delete thier group")
        return redirect('/dashboard')


def allGroups(request):
    if not 'user_id' in request.session:
        return redirect("/")
   # allGroups = Group.objects.exclude(user)
    user = Users.objects.get(id=request.session['user_id'])
    allGroups = Group.objects.exclude(owner=user.id)

    context = {
    #        "allGroups": allGroups,
            "allGroups": allGroups,
            "user": user,
    }
    return render(request, "allGroups.html", context)



#-------------END------------------------------




#-----------CONNOR VIEWS------------------------
def edit(request, group_id):
    if 'user_id' in request.session:
        this_owner=request.session['user_id']
        if Group.objects.filter(id=group_id, owner=this_owner):
            a_group = Group.objects.get(id=group_id)
            context = {
                'group': a_group
            }
            return render(request, 'edit.html', context)
    else:
        return redirect('/')
    
def update(request, group_id):
    errors = Group.objects.GroupManager(request.POST)
    if len(errors) > 0 :
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('edit/{group_id}')
    to_update = Group.objects.get(id=group_id)
    to_update.group_name = request.POST['name']
    to_update.group_genre = request.POST['genre']
    to_update.time_date = request.POST['time_date']
    to_update.save()
    return redirect('/')


def group_chat(request, group_id):
    if 'user_id' in request.session:
        this_member=request.session['user_id']
        if Group.objects.filter(id=group_id, member=this_member):
            a_group = Group.objects.get(id=group_id)
            group_messages = Wall_Message.objects.filter(group_id = group_id)
            context = {'group':a_group, 'group_messages': group_messages}
        return render(request, 'group_chat.html', context)
    else:
        return redirect('/')
    
def post_mess(request, group_id):
    Wall_Message.objects.create(
        message=request.POST['mess'],
        poster=User.objects.get(id=request.session['user_id']),
        group=Group.objects.get(id=group_id)
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#--------------END--------------------------



#-------------GUSTAVO VIEWS---------------------
def new(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = Users.objects.get(id = request.session['user_id'])
    return render(request, 'create.html')

def create(request):
    if request.method == 'POST':
        errors = Group.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect("/new")  
        else:
            x = Group.objects.create(
                name=request.POST['name'], 
                genre=request.POST['genre'], 
                desc=request.POST['desc'], 
               # owner=request.POST['owner'], 
                owner = Users.objects.get(id=request.session['user_id']))
            x.save()
    return redirect("/dashboard")

def users_groups(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    current_user = Users.objects.get(id=request.session['user_id'])
    return render(request, 'other_user_groups.html',)
#---------------END--------------------------
