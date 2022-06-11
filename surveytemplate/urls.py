from django.urls import path
from . import views

urlpatterns = [
    
    path('home/',views.HomeView.as_view(), name='home'),
    path('groups/',views.GroupsView.as_view(), name='groups'),
    path('templates/',views.TemplateListView.as_view(), name='templates'),
    path('create/',views.CreateTemplate.as_view(),name = 'create'),
    path('edit/<str:pk>/',views.EditTemplate.as_view(), name='edit'),
    path('delete/<str:pk>/', views.DeleteTemplate.as_view(),name = 'delete'),

    path('recepients/',views.RecepientView.as_view(), name='recepients'),
    path('groups/<int:pk>',views.GroupView.as_view(), name='group-view'),
    path('upload/',views.UploadFiles.as_view(), name='upload'),
    path('download/',views.DownloadRecepients.as_view(), name='download'),
    path('search/',views.SearchRecepients.as_view(), name='search'),
]
