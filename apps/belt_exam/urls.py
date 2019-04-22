from django.urls import path
from . import views
                    
urlpatterns = [
    path('main', views.main),
    path('travels', views.trips),
    path('register', views.register),
    path('login', views.login),
    path('travels/destination/<trip_id>', views.display_trip),
    path('logout', views.logout),
    path('travels/add', views.add_trip),
    path('create', views.create),
    path('join/<trip_id>', views.join)
]