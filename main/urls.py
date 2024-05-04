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

]
