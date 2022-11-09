from django.shortcuts import get_object_or_404, render, redirect

from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .forms import AddAuthorForm, EditReleaseForm, EditUserForm, RegisterUserForm, ReleaseForm, AddTopicForm
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.urls import reverse
from django.forms import formset_factory
from browse.models import Release, Author
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def userlogin(request):
    if request.method == 'POST' and len(request.POST['username']) > 0 and len(request.POST['password']) > 0:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, ('There was an error logging in. Try again...'))
            return redirect('login')
    else:
        return redirect('login')


def userlogout(request):
    logout(request)
    messages.success(request, ('You were logged out.'))
    return redirect('login')


def registration(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ('Registration successfull!'))
            return HttpResponseRedirect('/')
    else:
        form = RegisterUserForm()
    return render(request, 'registration/register.html', {
        'form': form,
    })


class UserRegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserProfile(TemplateView):
    template_name = 'account/profile.html'
    context_object_name = 'UserReleasesList'
    def get_queryset(self):
        return Release.objects.filter(owner = self.request.user)


def userprofile(request):
    releases = Release.objects.filter(owner = request.user)
    context = {'releases': releases}
    return render(request, 'account/profile.html', context)


class EditUserView(UpdateView):
    form_class = EditUserForm
    template_name = 'account/edit_profile.html'
    success_url = '/account/profile'

    def get_object(self):
        return self.request.user


def upload_work(request):
    form = ReleaseForm()
    if request.method == 'POST':
        form = ReleaseForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            form.save_m2m()
            return redirect(reverse('account:profile'))
            # return render(request, 'account/profile.html', {})
        else:
            messages.success(request, ('Tapahtui virhe. Yritä uudelleen.'))
    form = ReleaseForm()
    context = {'form': form}
    return render(request, 'works/upload_work.html', context)


def edit_release(request, id):
    context = {}
    obj = get_object_or_404(Release, id = id)
    form = EditReleaseForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.save()
        return redirect(reverse('account:profile'))

    context = {'form': form}
    return render(request, 'works/edit_release.html', context)


class EditReleaseView(UpdateView):
    form_class = EditReleaseForm
    template_name = 'account/edit_profile.html'
    success_url = '/account/profile'

    def get_object(self):
        release = Release.objects.filter(id = self.kwargs.get('id')).first()
        return release


def add_author(request):
    if request.method == 'POST':
        form = AddAuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ('Lisätty!'))
            return HttpResponseRedirect('upload_work')
        else:
            messages.success(request, ('Tapahtui virhe, yritä uudelleen.'))
            form = ReleaseForm()
    return render(request, 'works/upload_work.html', {
        'form': form,
    })

def add_topic(request):
    if request.method == 'POST':
        form = AddTopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ('Lisätty!'))
            return HttpResponseRedirect('upload_work')
        else:
            messages.success(request, ('Tapahtui virhe, yritä uudelleen.'))
            form = ReleaseForm()
    return render(request, 'works/upload_work.html', {
        'form': form,
    })



# AuthorFormset = inlineformset_factory(Release, Author, fields=('first_name', 'last_name'), fk_name='authors')

# class ReleaseUploadView(CreateView):
#     model = Release
#     fields = ['name', 'release_date', 'authors', 'description', 'file', 'cover']