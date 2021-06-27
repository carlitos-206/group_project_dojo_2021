from django.urls import path
from . import views

#everyone please write your urls within the given space so it's easy to identify the routes same in the Views.py file!!!!
#Also make sure to place " , "(comma) after all urls this will make debugin easier

urlpatterns=[
#-------URLS CARLOS----------------
    path('', views.index),
    path('new_user', views.register),
    path('terms', views.terms),
    path('sign_in', views.sign_in),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('goodbye', views.farewell),

#--------END------------------

#--------URLS JAIMEI-----------
#path('myGroups/<str:name>', views.myGroups),
path('myGroups', views.myGroups),
path('allGroups', views.allGroups),
path('allGroups/<int:id>/delete', views.allGroups_delete),
path('myGroups/<int:id>/delete', views.myGroups_delete),
######path('/myGroups/{{x.id}}/delete', views.myGroups_edit) - update/uncomment after Edit Page is completed by Connor

#--------END-----------


#-------URLS CONNOR------------

#------END-----------------------

#-----URLS GUSTAVO--------------
path('new', views.new),
path('create', views.create),
path('users_groups', views.users_groups)
#------END---------------
]