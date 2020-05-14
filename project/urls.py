from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', login_view, name="login_view"),
    path('login', login_view, name="login_view"),
    path('profile', profile_view, name="profile_view"),
    path('logout', logout_view, name="logout_view"),
    path('my_tasks', tasks_view, name="tasks_view"),
    path('interv_list/', interv_list, name='interv_list'),
    path('intervention/<int:pk>/fill_params/', views.fill_params, name='fill_params'),
    path('intervention/<int:pk>/', interv_detail, name='interv_detail'),
    path('intervention/<int:pk>/add_parameters/', add_parameters, name='add_parameters'),
    path('intervention/<int:pk>/fill_research/<int:res_pk>', fill_research, name='add_research'),
    path('intervention/<int:pk>/create_template/', create_templ, name='create_template'),
    path('intervention/<int:pk>/create_formula/', create_formula, name='create_formula'),
    path('intervention/<int:pk>/template_detail/', template_detail, name='template_detail'),
    path('intervention/<int:interv_pk>/research_detail/<int:res_pk>', research_detail, name='research_detail'),
    path('intervention/<int:interv_pk>/research_tasks', research_tasks, name='research_tasks'),
    path('our_researches', our_researches, name='our_researches')

]
