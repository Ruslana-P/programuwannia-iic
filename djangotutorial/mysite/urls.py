from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("polls/", include("polls.urls")), # use include() for including other URL patterns
    path('machine_era/', include('machine_era.urls')),
    path('admin/', admin.site.urls), # pre-built URLconf provided by Django for the default admin site.
]

# --- DEBUG TOOLBAR CONFIGURATION (Conditional Inclusion) ---
if settings.DEBUG:
    import debug_toolbar 
    
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)