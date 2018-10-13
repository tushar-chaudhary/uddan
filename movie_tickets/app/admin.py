#This file is used to register the models to the backend admin panel so that it can be visible

from django.contrib import admin
from .models import Movie_details

admin.site.register(Movie_details)
