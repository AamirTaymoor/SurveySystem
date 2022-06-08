from django.urls import path
from . import views

urlpatterns = [
    
    path('home/',views.HomeView.as_view(), name='home'),
    path('templates/',views.TemplateListVew.as_view(), name='templates'),
    path('create/',views.CreateTemplate.as_view(),name = 'create'),
    path('edit/<str:pk>/',views.EditTemplate.as_view(), name='edit'),
    path('delete/<str:pk>/', views.DeleteTemplate.as_view(),name = 'delete'),

]
