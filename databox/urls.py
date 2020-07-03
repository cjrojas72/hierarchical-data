from django.urls import path
from databox import views

urlpatterns = [
    path('', views.index)
]
