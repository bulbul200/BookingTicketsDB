from django.urls import path, include
from . import views 
urlpatterns = [

    path("seats", views.passengerCount.as_view()),
    path('schedules/', views.SchedulesView.as_view()),
    path('car/', views.SearchCar.as_view()),
    path('routes/', views.searchRoutes.as_view()),
    path('passenger/', views.PassengersView.as_view()),
    
]