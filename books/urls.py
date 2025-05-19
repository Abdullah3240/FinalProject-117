"""
urls.py

Project Gutenberg Word Frequency Web App
Author: Abdullah Bataineh
Date: 5/16/2025

Maps URL paths to view functions. Currently routes the root URL
to the homepage view for book search and processing.
"""
# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
