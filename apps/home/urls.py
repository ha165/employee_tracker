

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # employee view
    path("employee/",views.employee,name='employee'),
    
    #add_user/employess
    path('add-user/', views.add_user, name='add_user'),

    path('update-profile/', views.update_profile, name='update_profile'),

    path("kpi/",views.kpi,name='kpi'),

    path('kpi/add/', views.add_kpi, name='add_kpi'),

    path('review-cycles/', views.review_cycle, name='review_cycle'),

    path('review-cycles/add/', views.add_review_cycle, name='add_review_cycle'),

    path('performance-reviews/', views.performance_reviews, name='performance_reviews'),

    path('performance-reviews/add/', views.add_performance_review, name='add_performance_review'),

    path('api/kpi-completion-all-users/', views.kpi_completion_all_users, name='kpi-completion-all-users'),

    path('api/employee-kpi-performance/', views.employee_kpi_performance, name='employee-kpi-performance'),

    path('api/employee-performance-trend/', views.employee_performance_trend, name='employee-performance-trend'),

    path('api/kpi-performance-pie-chart/', views.kpi_performance_pie_chart, name='kpi-performance-pie-chart'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
