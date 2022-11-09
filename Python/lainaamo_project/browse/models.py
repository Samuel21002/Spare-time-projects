from __future__ import annotations
from datetime import datetime
from django.conf import settings
from django.db import models
from django.db.models.functions import Round
from django.db.models import Avg
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.validators import FileExtensionValidator, validate_image_file_extension

""" Palauttaa jokaisen sanan ensimmäisen kirjaimen isona """
def capitalize(line):
    return ' '.join(s[:1].upper() + s[1:] for s in line.split(' '))
    

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    """ Palauttaa "kapitalisoituneena" etu- ja sukunimen """
    def __str__(self) -> str:
        return capitalize(f"{self.first_name} {self.last_name}")

class Topic(models.Model):
    topic_name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.topic_name

class Release(models.Model):
    name = models.CharField(max_length=100)
    release_date = models.DateTimeField()
    authors = models.ManyToManyField(Author)
    topics = models.ManyToManyField(Topic, null=True, blank=True)
    description = models.CharField(max_length=400)
    file = models.FileField(upload_to='static', null=True, blank=True, validators=[FileExtensionValidator( ['pdf'] ) ])
    cover = models.ImageField(upload_to='static', null=True, blank=True, validators=[validate_image_file_extension])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    @property
    def release_reviews(self):
        release_ratings = Review.objects.all().filter(release_id = self.id)
        rounded_rating = round(sum(release_ratings) / len(release_ratings))
        print(rounded_ratings)
        return rounded_ratings

    @property
    def average_rating(self):
        return Review.objects.all().filter(release_id = self.id).aggregate(average = Round(Avg('rating'))).get('average')

class Review(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, null=True, blank=True)
    release = models.ForeignKey(Release, models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    verbal_review = models.TextField(max_length=400)

    def __str__(self):
        return f"{self.rating}"

    # """ Tähän keskiarvo kaikista tuotteen arvioinneista """
    @property
    def get_release_name(self):

        release = Release.objects.all().get(id = self.release_id)
        return release.name



RETURN_DELTA = 14  # Päivien määrä kunnes lainaus umpeutuu. (Muuta tästä tarpeen mukaan!!)

""" Asettaa palautuspäivän 'RETURN_DELTA' päivän päähän automaattisesti Rental-objektin luomisen yhteydessä """
def set_due_date(rental_date):
    delta = timezone.timedelta(rental_date) 
    return datetime.now() + delta  

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    release = models.ForeignKey(Release, on_delete=models.CASCADE)
    rental_date = models.DateTimeField(default=timezone.now())
    return_date = models.DateTimeField(default=set_due_date(RETURN_DELTA))
    returned = models.BooleanField(default=False)

    
    """ Hakee release_id:n perusteella lainatun teoksen nimen """
    @property
    def name_of_release(self):
        release_object = Release.objects.get(pk = self.release_id)
        return release_object.name


    """ Palauttaa lainauksen tilan riippuen palautusajankohdasta (tunteina) """
    @property
    def status_of_rental(self) -> str:

        difference = self.return_date - timezone.now()  # muuttuja kuvailee eräpäivän ja nykyisen päivän välistä eroa
        difference_in_hours = difference.total_seconds() / 3600  # muuttaa erotuksen tunneiksi
        
        if not self.returned:
            if difference_in_hours <= 0:
                return 'Myöhässä'
                #return ('Erääntynyt', '#9e3f3f')
            elif 0 < difference_in_hours < 120:
                return f'Erääntymässä'
                #return ('Erääntymässä', '#d3cd56')
            elif difference_in_hours > 120:
                return 'Lainassa'
                #return ('Ei erääntynyt', '#3f9e53')
        else:
            return 'Palautettu'

    @property
    def left_of_lend(self) -> str:
        
        difference = self.return_date - timezone.now()  # muuttuja kuvailee eräpäivän ja nykyisen päivän välistä eroa

        days = difference.days
        seconds = difference.seconds
        hours = seconds//3600
        minutes = (seconds//60)%60

        if days > 0:
            return f"Jäljellä: {days}pv {hours}t {minutes}min"

        else:
            return f"Myöhässä: {abs(days)}pv {hours}t {minutes}min"

            


