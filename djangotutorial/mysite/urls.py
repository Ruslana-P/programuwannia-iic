from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("polls/", include("polls.urls")), # use include() for including other URL patterns
    path('admin/', admin.site.urls), # pre-built URLconf provided by Django for the default admin site.
]
