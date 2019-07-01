"""Platzigram URLs."""

from django.contrib import admin
from django.urls import path

from platzigram import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello-world/', views.hello_world, name='hello-world'),
    path('sort-numbers/', views.sort_numbers, name='sort-numbers'),
    path('hi/<name>/<int:age>/', views.say_hi, name='hi'),
]
