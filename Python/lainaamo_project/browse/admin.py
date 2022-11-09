from django.contrib import admin
from .models import Release, Author, Topic, Review, Rental

# class AuthorInline(admin.TabularInline):
#     model = Author
#     extra = 1

class ReleaseAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Julkaisija',      {'fields': ['owner']}),
        ('Nimi',            {'fields': ['name']}),
        ('Tekijä',          {'fields': ['authors']}),
        ('JulkaisuPäivä',   {'fields': ['release_date']}),
        ('Kuvaus',          {'fields': ['description']}),
        ('Tiedosto',        {'fields': ['file']}),
        ('Kuva',            {'fields': ['cover']}),
        ('Tyyppi',          {'fields': ['topics']})
    ]

    list_display = ('id', 'name', 'release_date', 'description', 'file', 'owner_id')
    list_filter = ['release_date', 'authors', 'topics']
    search_fields = ['name']

class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Etunimi',    {'fields': ['first_name']}),
        ('Sukunimi',   {'fields': ['last_name']})
    ]

    list_display = ('first_name', 'last_name')
    search_fields = ['first_name', 'last_name']

class TopicAdmin(admin.ModelAdmin):

    list_display = ('topic_name',)
    search_fields = ['topic_name']

class ReviewAdmin(admin.ModelAdmin):

    list_display = ('user', 'rating', 'verbal_review', 'release')
    search_fields = ['verbal_review']
    list_filter = ['rating']

class RentalAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'name_of_release', 'release_id', 'rental_date', 'return_date')
    search_fields = ['user']
    fieldsets = [

    ('Nimi',            {'fields': ['user']}),
    ('Julkaisu ID',     {'fields': ['release']}),
    ('Lainapäivä',      {'fields': ['rental_date']}),
    ('Palautuspäivä',   {'fields': ['return_date']}),
    ('Palautettu',      {'fields': ['returned']})
    ]
    list_filter = ['return_date', 'returned']

admin.site.register(Release, ReleaseAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Rental, RentalAdmin)