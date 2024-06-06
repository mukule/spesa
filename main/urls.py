from django.urls import path
from . import views


app_name = 'main'
urlpatterns = [
    path("", views.index, name="index"),
    path("choices/", views.choice, name="u"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("blogs/", views.blogs, name="blogs"),
    path("consultant/", views.consultant, name="consultant"),
    path('consult/<int:speciality_id>/',
         views.create_consult, name='consult'),
    path('fconsult/<int:concern_id>/', views.create_f_consult, name='fconsult'),
    path('mpesa_callback/', views.mpesa_callback, name='mpesa_callback'),
    path('success/', views.success, name='success'),
    path('fail/', views.fail, name='fail'),
    path('consult/toggle-task/<int:consult_id>/',
         views.toggle_task_acceptance, name='task_acceptance'),
    path('task/<int:consult_id>/', views.consult_detail, name='task_detail'),
    path('consult/<int:consult_id>/create-response/',
         views.create_response, name='create_response'),
    path('response/<int:response_id>/',
         views.response_detail, name='response_detail'),



]
