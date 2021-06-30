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
    path('drop/<int:group_id>', views.dropGroup),

#--------END------------------

#--------URLS JAIMEI-----------
#path('myGroups/<str:name>', views.myGroups),
path('myGroups', views.myGroups),
path('allGroups', views.allGroups),
path('myGroups/<int:group_id>/delete', views.myGroups_delete),
path('myGroups/<int:group_id>/edit', views.edit),
#--------END-----------


#-------URLS CONNOR------------
    path('edit/<int:group_id>', views.edit),
    path('group/<int:group_id>/update', views.update),
    path('group_chat/<int:group_id>', views.group_chat),
    path('process_message/<int:group_id>', views.post_mess),
#------END-----------------------

#-----URLS GUSTAVO--------------
path('new', views.new),
path('create', views.create),
path('users_groups/<int:group_owner_id>', views.users_groups),
path('join/<int:group_id>', views.join)
#------END---------------
]