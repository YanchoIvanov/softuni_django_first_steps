from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.managers import DirectorManager
from main_app.mixins import LastUpdatedMixin, IsAwardedMixin


class PersonBase(models.Model):
    full_name = models.CharField(max_length=120, validators=[MinLengthValidator(2)])
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')

    class Meta:
        abstract = True


class Director(PersonBase):
    years_of_experience = models.SmallIntegerField(validators=[MinValueValidator(0)], default=0)

    objects = DirectorManager()


class Actor(PersonBase, LastUpdatedMixin, IsAwardedMixin):
    pass


class Movie(LastUpdatedMixin, IsAwardedMixin):
    GENRE_CHOICES = [
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other'),
    ]

    title = models.CharField(validators=[MinLengthValidator(5)], max_length=150)
    release_date = models.DateField()
    storyline = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=6, default='Other', choices=GENRE_CHOICES)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[
        MinValueValidator(0.0), MaxValueValidator(10.0)], default=0.0)
    is_classic = models.BooleanField(default=False)
    director = models.ForeignKey(to=Director, on_delete=models.CASCADE, related_name='director_movies')
    starring_actor = models.ForeignKey(to=Actor, blank=True, null=True, on_delete=models.SET_NULL,
                                       related_name='starring_movies')
    actors = models.ManyToManyField(to=Actor, related_name='actor_movies')


