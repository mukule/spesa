from django.urls import path
from . import views


app_name = 'adminstration'
urlpatterns = [
    path("admin/", views.dashboard, name="admin"),
    path("create-speciality/", views.create_speciality, name="create_speciality"),
    path('speciality/edit/<int:speciality_id>/',
         views.edit_speciality, name='edit_speciality'),
    path('speciality/delete/<int:speciality_id>/',
         views.delete_speciality, name='delete_speciality'),
    path("create-financial_concern/", views.create_financial_concern,
         name="create_financial_concern"),
    path('edit-concern/<int:concern_id>/',
         views.edit_financial_concern, name='edit_financial_concern'),
    path('delete-concern/<int:concern_id>/',
         views.delete_financial_concern, name='delete_financial_concern'),
    path("create_about/", views.create_about, name="create_about"),
    path('edit-about/<int:about_id>/', views.edit_about, name='edit_about'),
    path('delete-about/<int:about_id>/',
         views.delete_about, name='delete_about'),
    path("create-panel/", views.create_panel, name="create_panel"),
    path('edit-panel/<int:panel_id>/', views.edit_panel, name='edit_panel'),
    path('delete-panel/<int:panel_id>/',
         views.delete_panel, name='delete_panel'),
    path("create-works/", views.create_works, name="create_works"),
    path('edit-works/<int:works_id>/', views.edit_works, name='edit_works'),
    path('delete-works/<int:works_id>/',
         views.delete_works, name='delete_works'),
    path("create_category/", views.create_category, name="create_category"),
    path('category/<int:category_id>/edit/',
         views.edit_category, name='edit_category'),
    path('category/<int:category_id>/delete/',
         views.delete_category, name='delete_category'),
    path('category/<int:category_id>/',
         views.category_detail, name='category_detail'),
    path('create_blog/<int:category_id>/',
         views.create_blog, name='create_blog'),
    path('<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),
    path('<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),

]
