from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [

  path('users/create/client', views.create_client, name='create_client'),
  path('users/create/serviceprovider',views.create_serviceprovider, name='create_serviceprovider'),

  path('users/authenticate/client', obtain_auth_token, name='authenticate_client'),
  path('users/authenticate/serviceprovider', obtain_auth_token, name='authenticate_serviceprovider'),

  path('users/logout', views.Logout, name='user_logout'),

  #start of service views,urls
  path('service/create',views.createService, name="createService"),
  path('service/list',views.listService, name="listService"),
  path('service/list/provider/<int:providerId>',views.listByProviderId, name="listByProviderId"),
  path('service/list/<int:pk>',views.listById, name="listById"),
  path('service/edit/<int:pk>',views.editList, name="editList"),
  path('service/delete/<int:pk>',views.deleteList, name="deleteList"),
  
] 