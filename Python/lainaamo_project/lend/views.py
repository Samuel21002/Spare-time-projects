from django.shortcuts import render
from browse.models import Rental
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models.functions import Lower

@login_required
def index(request):

    context = {}
    user_rental_objects = Rental.objects.all().filter(user=request.user)
    objects_on_rent = []
    objects_returned = []
    most_recent_rent = []
    
    if user_rental_objects:

        objects_on_rent = user_rental_objects.filter(returned = False)
        objects_returned = user_rental_objects.filter(returned = True)
        most_recent_rent = max(date.rental_date for date in user_rental_objects)

    # Järjestää lainat nimen tai palautuspäivän perusteella
    sort = request.GET.get('sorting')
    
    if sort == "by_name":
        objects_on_rent = objects_on_rent.order_by(Lower('release__name'))
        objects_returned = objects_returned.order_by(Lower('release__name'))
    elif sort == "by_return_date":
        objects_on_rent = objects_on_rent.order_by('return_date')
        objects_returned = objects_returned.order_by('return_date')

    context = {
        'user_rental_objects': user_rental_objects,
        'on_rent' : objects_on_rent,
        'returned' : objects_returned,
        'most_recent' : most_recent_rent
        }

    return render(request, 'lend/index.html', context)

""" Lisää teoksen palautuksiin """
def add_to_returned(request, id):

    user_rental_objects = Rental.objects.all().filter(user=request.user)
    context = {'user_rental_objects' : user_rental_objects}

    if request.POST:
        try:
            rental = Rental.objects.get(pk = id)
            rental.returned = True
            rental.save()
            messages.success(request, 'Kiitos lainasta!')
        except:
            messages.error(request, 'Tapahtui virhe, yritä uudelleen!')

    return HttpResponseRedirect(reverse('lend:lend'))


def error_404(request, exception):
    return render(request, 'core/404.html')

def pdf(request):
    return render(request, 'lend/pdf.html')