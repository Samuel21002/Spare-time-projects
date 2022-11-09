"""lainaamo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500
from . import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', include('core.urls')),
    path('browse/', include('browse.urls')),
    path('lend/', include('lend.urls')),
    path('account/', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('oauth/', include('social_django.urls', namespace='social')),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.handler404'
# handler500 = 'core.views.handler500'