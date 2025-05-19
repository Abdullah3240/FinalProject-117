"""
admin.py

Project Gutenberg Word Frequency Web App
Author: Abdullah Bataineh
Date: 5/18/2025

Registers the Book and FrequentWord models with the Django Admin interface
so they can be managed through the browser.
"""


from django.contrib import admin
from .models import Book, FrequentWord
# Register your models here.

admin.site.register(Book)
admin.site.register(FrequentWord)
