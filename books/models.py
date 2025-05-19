"""
models.py

Project Gutenberg Word Frequency Web App
Author: Abdullah Bataineh
Date: 5/16/2025

Defines the database models:
- Book: stores book title
- FrequentWord: stores top 10 words and their frequencies for each book
"""



from django.db import models

class Book(models.Model):
    """
    Represents a book stored in the local database.
    Fields:
        title (str): The title or identifier of the book.
    """
    title = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """ String representation of the Book model.
        Returns:
            str: The title of the book.
        """
        return self.title

class FrequentWord(models.Model):
    """
    Represents one of the top 10 most frequent words in a book.
    Fields:
        book (ForeignKey): Reference to the related Book object.
        word (str): The frequent word.
        frequency (int): Number of times the word appears in the book.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='words')
    word = models.CharField(max_length=50)
    frequency = models.IntegerField()

    def __str__(self):
        """
        String representation of the FrequentWord object.
        """
        return f"{self.word} ({self.frequency})"
