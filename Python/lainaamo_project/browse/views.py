from platform import release
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from .models import Release, Author, Rental, Topic, Review
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


PAGER_PER_SITE = 5  # Määrittää hakutuloksien määrän per sivu

""" Etusivu, jossa hakutoiminto. Hakutulokset palauttavat osittaisnäkymän details_partial.html jokaista tulosta kohden """
def index_page(request):

    topics = Topic.objects.all()
    context = {'topics' : topics}
    msg = ""

    # Alustaa hakutoiminnon
    if request.method == 'GET':
        
        multiple_q = Q()
        query_name = request.GET.get("search")
        query_topic_id = request.GET.get("topics")
        
        if query_name:  # Jos haku tapahtuu teoksen tai tekijän perusteella

            multiple_q |= Q(Q(name__contains=query_name) | 
            Q(authors__first_name__contains=query_name) | Q(authors__last_name__contains=query_name))

        if query_topic_id and query_topic_id is not '-- Kaikki Aiheet --':  # Jos haku tapahtuu aiheen perusteella

            multiple_q &= Q(topics__id__exact = query_topic_id)
            
        queried_releases = Release.objects.filter(multiple_q).order_by('name').distinct()
        if multiple_q:
            msg = f"Haullasi löytyi {len(queried_releases)} tulosta"

        paginated_filtered_releases = Paginator(queried_releases, PAGER_PER_SITE)
        page_number = request.GET.get('page', 1)

        try:
            page_obj = paginated_filtered_releases.page(page_number)
        except PageNotAnInteger:
            page_obj = paginated_filtered_releases.page(PAGER_PER_SITE)
        except EmptyPage:
            page_obj = paginated_filtered_releases.page(paginated_filtered_releases.num_pages)

        context.update({'releases' : queried_releases, 'msg' : msg, 'pagination_obj' : page_obj, 'query' : query_name })

    else:
        queried_releases = Release.objects.all().order_by("-release_date")
        context.update({'releases' : queried_releases})

    return render(request, 'browse/index.html', context)
    

""" Teoksen lisätietosivu. Ottaa parametriksi teoksen id:n. 
    Mikäli kirjautunut käyttäjä on jo arvostellut kyseistä, palautuu has_reviewed totena, jolloin teosta ei voi enää arvioida. """
def detail(request, id):

    context = {}

    release = get_object_or_404(Release, id=id)
    top_reviews = Review.objects.all().filter(release_id = id).order_by('-rating')[:3]

    has_reviewed = False

    if request.user.is_authenticated:
        if Review.objects.all().filter(user=request.user, release_id=id):
            has_reviewed = True
            context.update({'has_reviewed': has_reviewed})

    context.update({'rel': release, 'top_reviews' : top_reviews})

    return render(request, 'browse/details_full.html', context)


""" Lisää teoksen lainoihin. Ottaa parametriksi teoksen id:n."""
def add_to_db(request, id):

    if request.POST:
        
        try:
            check_user_rentals = Rental.objects.all().filter(user = request.user, release_id=id, returned=False)  # Etsii onko lainassa olevaa jo lainattuja teoksia

        except Rental.DoesNotExist:
            check_user_rentals = None

        if check_user_rentals.exists():

            messages.error(request, ('Sinulla on jo tämä lainaus'))
            return HttpResponseRedirect(reverse('browse:release_details', kwargs={'id': id}))

        else:
            rental = Rental.objects.create(release_id=id, user=request.user)  # Jos teos ei ole lainassa, lisää lainaus tietokantaan
            rental.save()
            return HttpResponseRedirect(reverse('lend:lend'))

""" Lisää käyttäjän arvostelun tietokantaan. Mikäli kirjautuneen käyttäjän has_reviewed bool-muuttuja ei ole tosi, voidaan teos arvioida"""
def post_review(request, id):

    if request.method == 'POST':

        try:
            user = request.user
            release = Release.objects.get(id = id)
            rate = request.POST.get('rating')
            comment = request.POST.get('comment')

            Review(user=user, release=release, rating=rate, verbal_review=comment).save()
            messages.error(request, ('Kiitos arviosta!'))

        #NULLCHECK
        except:
            messages.error(request, ('Jokin meni pieleen, yritä uudelleen!'))

        return HttpResponseRedirect(reverse('browse:release_details', kwargs={'id': id}))