# from socket import fromshare
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from browse.models import Author, Release, Topic
from django.db import models
from django.forms.models import inlineformset_factory
from django.forms import MultiWidget,TextInput

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

# class EditUserForm(UserChangeForm):
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)



class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'


class ReleaseForm(forms.ModelForm):
    class Meta:
        model = Release
        widgets = {
            'name': forms.TextInput(),
            'release_date': DateInput(),
            'description': forms.Textarea(),
            }
        fields = ('name', 'authors', 'topics', 'release_date', 'description', 'file', 'cover')


class EditReleaseForm(forms.ModelForm):
    class Meta:
        model = Release
        widgets = {
            'name': forms.TextInput(),
            'release_date': DateInput(),
            'description': forms.Textarea(),
            }
        fields = ('name', 'authors', 'topics', 'release_date', 'description')
