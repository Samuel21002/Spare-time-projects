from django import urls
from django.urls import path
from . import views
from django.conf import settings
from django.urls import re_path as url
from django.conf.urls.static import static

app_name = 'lend'
urlpatterns = [
    path('', views.index, name='lend'),
    path('<int:id>/add_to_returned', views.add_to_returned, name='add_to_returned')
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)