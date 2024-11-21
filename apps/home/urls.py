

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # employee view
    path("employee/",views.employee,name='employee'),
    
    #add_user/employess
     path('add-user/', views.add_user, name='add_user'),

     path("kpi/",views.kpi,name='kpi'),

      path('add-kpi/', views.add_kpi, name='add_kpi'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
