from django.urls import path
from . import views
from django.urls import reverse

app_name = 'browse'
urlpatterns = [
    path('', views.index_page, name='browse'),
    path('<int:id>/details/', views.detail, name='release_details'),
    path('<int:id>/details/add_to_db/', views.add_to_db, name='add_to_db'),
    path('<int:id>/details/post_review/', views.post_review, name='post_review'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]