"""
views.py

Project Gutenberg Word Frequency Web App
Author: Abdullah Bataineh
Date: 5/16/2025

This file handles all view logic, including:
- Searching for book titles in the local SQLite database
- Fetching books from Project Gutenberg using a URL
- Extracting and storing the top 10 most frequent words
- Displaying results on the homepage
"""

import requests
from django.shortcuts import render
from .models import Book, FrequentWord
from collections import Counter
import re

def clean_text(text):
    """ Clean and tokenize plain text from the book.
    Removes non-alphabetic characters, converts to lowercase, and splits into words.
    Args:
        text (str): The raw book content.
    Returns:
        list: A list of cleaned words.
    """
    text = re.sub(r'[^A-Za-z\s]', '', text)  # remove punctuation
    words = text.lower().split()
    return words

def home(request):
    """ Main view that handles both title and URL search requests.
    - If a book title is entered, it tries to fetch from the local database.
    - If a Project Gutenberg URL is entered, it downloads the book, extracts frequent words,
      saves to the database, and displays them.
    Args:
        request (HttpRequest): The HTTP request from the browser.
    Returns:
        HttpResponse: Renders the home.html template with context data.
    """
    context = {}

    if request.method == "POST":
        if 'title_search' in request.POST:
            title = request.POST.get('title')
            try:
                book = Book.objects.get(title=title)
                words = book.words.all().order_by('-frequency')[:10]
                context['words'] = words
                context['source'] = 'Database'
            except Book.DoesNotExist:
                context['error'] = "Book not found in database."

        elif 'url_search' in request.POST:
            raw_url = request.POST.get('url')

            try:
                if not raw_url:
                    raise ValueError("No URL provided.")

                # Step 1: Convert normal Gutenberg link to .txt link
                if "/ebooks/" in raw_url:
                    book_id = raw_url.strip().split("/ebooks/")[-1].strip("/")
                    txt_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
                else:
                    txt_url = raw_url

                # Step 2: Download book text
                response = requests.get(txt_url)
                response.raise_for_status()
                text = response.text

                # Step 3: Extract book title
                title = None
                for line in text.splitlines():
                    if line.strip().lower().startswith("title:"):
                        raw_title = line.split(":", 1)[1].strip()
                        title = raw_title.split(";")[0].strip() 

                        break

                if not title:
                    title = f"Gutenberg Book {book_id}"  # fallback title

                print("DEBUG: Title extracted →", title)

                # Step 4: Clean and count words
                words = clean_text(text)
                most_common = Counter(words).most_common(10)

                print("DEBUG: Top words →", most_common)

                # Step 5: Save book and words
                book, created = Book.objects.get_or_create(title=title)
                book.words.all().delete()  # Clear previous

                for word, freq in most_common:
                    FrequentWord.objects.create(book=book, word=word, frequency=freq)

                # Step 6: Show results
                context['words'] = book.words.all().order_by('-frequency')[:10]
                context['source'] = 'Web (Project Gutenberg)'
                context['saved_title'] = title

            except Exception as e:
                context['error'] = f"Error downloading or processing book: {str(e)}"





    return render(request, 'books/home.html', context)
