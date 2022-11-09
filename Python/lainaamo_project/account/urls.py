from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    path('userlogin', views.userlogin, name='login'),
    path('userlogout', views.userlogout, name='logout'),
    path('registration', views.registration, name='registration'),
    # path('profile', views.UserProfile.as_view(), name='profile'),
    path('profile', views.userprofile, name='profile'),
    path('edit_profile/', views.EditUserView.as_view(), name='edit_profile'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    # path('upload_work/', views.ReleaseUploadView.as_view(), name='upload')
    path('upload_work/', views.upload_work, name='upload'),
    path('add_author', views.add_author, name='add_author'),
    path('add_topic', views.add_topic, name='add_topic'),
    # path('<int:id>/edit_release/', views.edit_release, name='edit_release'),
    path('<int:id>/edit_release/', views.EditReleaseView.as_view(), name='edit_release'),
]