from django.urls import path
from . import views

urlpatterns = [
    path('interv_list', views.interv_list, name='interv_list'),
    path('intervention/<int:pk>/fill_params/', views.fill_params, name='fill_params'),
    path('intervention/<int:pk>/', views.interv_detail, name='interv_detail'),
    path('intervention/add/', views.interv_add, name = 'interv_add'),
    path('intervention/<int:pk>/edit/', views.interv_edit, name='interv_edit'),
    path('intervention/<int:pk>/add_parameters/', views.add_parameters, name='add_parameters'),
    path('intervention/<int:pk>/add_research/', views.add_research, name='add_research'),
    path('intervention/<int:pk>/create_template/', views.create_templ, name='create_template'),
    path('intervention/<int:pk>/create_formula/', views.create_formula, name='create_formula'),
    path('intervention/<int:pk>/template_detail/', views.template_detail, name='template_detail'),
    path('intervention/<int:interv_pk>/research_detail/<int:res_pk>', views.research_detail, name='research_detail'),

]
