from platform import release
from django.shortcuts import render
from django.db.models import Avg
from django.db.models.functions import Round
from browse.models import Release, Topic, Review



def index(request):
    
    topics = Topic.objects.all() 
    all_releases = Release.objects.all()
    top_releases = {}

    # Keskiarvo tuotteiden arvostelusta
    # for obj in Release.objects.all():
    #     top_releases[f'{obj.name}']=Review.objects.filter(release_id=obj.id).aggregate(rating = Round(Avg('rating')))
        
    print(top_releases)

    context = {'topics' : topics, 'all_releases' : all_releases, 'top_releases': top_releases}
    return render(request, 'core/index.html', context)

def handler404(request, exception):
    return render(request, 'core/404.html')

# def handler500(request, exception):
#     return render(request, 'core/500.html')
