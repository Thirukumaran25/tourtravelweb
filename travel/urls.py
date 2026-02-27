from django.urls import path
from .views import *


urlpatterns = [
   path('',home ,name='home'),
   path('about/',about ,name='about'),
   path('car/', car ,name='car'),
   path('car/<int:pk>/', vehicle_detail ,name='vehicle_detail'),
   path('tour/',tour ,name='tour'),
   path('tour/<slug:slug>/', tour_detail, name='tour_detail'),
   path('booking/',booking ,name='booking'),
   path('contact/',contact ,name='contact'),
   path('service/',service ,name='service'),
]