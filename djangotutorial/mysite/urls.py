from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("polls/", include("polls.urls")), # use include() for including other URL patterns
    path('admin/', admin.site.urls), # pre-built URLconf provided by Django for the default admin site.
]

# --- DEBUG TOOLBAR CONFIGURATION (Conditional Inclusion) ---
if settings.DEBUG:
    # 1. Import debug_toolbar
    import debug_toolbar 
    
    # 2. Prepend the debug toolbar's URLs to urlpatterns
    #    The 'debug_toolbar.urls' module contains the URL patterns list.
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

