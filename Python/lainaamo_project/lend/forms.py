from django import forms
from browse.models import Release

class ReleaseForm(forms.ModelForm):
  class Meta:
    model = Release
    fields = ('name', 'release_date', 'authors', 'description', 'file', 'cover')