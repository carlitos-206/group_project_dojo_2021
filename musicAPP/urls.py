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

#--------END-----------


#-------URLS CONNOR------------
    path('edit/<int:group_id>', views.edit),
    path('update/<int:group_id>', views.update),
#------END-----------------------

#-----URLS GUSTAVO--------------

#------END---------------
]