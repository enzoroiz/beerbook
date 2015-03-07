from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.template.defaultfilters import slugify

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class BeerType(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name


class BeerProducer(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # relationships
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username


class Beer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    introduced = models.DateField()
    image = models.ImageField(upload_to='beer_images', blank=True)
    country = CountryField(blank_label='(select country)')
    slug = models.SlugField(unique=True)

    # relationships
    type = models.ForeignKey(BeerType)
    producer = models.ForeignKey(BeerProducer)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Beer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=5, decimal_places=3)
    longitude = models.DecimalField(max_digits=5, decimal_places=3)
    country = CountryField(blank_label='(select country)')

    # relationships
    city = models.ForeignKey(City)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('latitude', 'longitude')


class Pub(models.Model):
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)  # need unique on field combo
    description = models.TextField()
    established = models.DateField()
    image = models.ImageField(upload_to='pub_images', blank=True)
    slug = models.SlugField(unique=True)

    # relationships
    location = models.ForeignKey(Location)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pub, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'location')


class Event(models.Model):
    title = models.CharField(max_length=128)
    datetime = models.DateTimeField()
    description = models.TextField()

    # relationships
    location = models.ForeignKey(Location)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'datetime')


class PubStockItem(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # relationships
    stocked_item = models.ForeignKey(Beer)
    stocked_at = models.ForeignKey(Pub)

    class Meta:
        unique_together = ('stocked_item', 'stocked_at')


class Rating(models.Model):
    rating = models.IntegerField(default=0)
    review = models.TextField()

    # relationships
    owner = models.ForeignKey(User)
    rated_beer = models.ForeignKey(Beer)

    class Meta:
        unique_together = ('owner', 'rated_beer')


class FriendListItem(models.Model):
    user_one = models.ForeignKey(User, related_name='friend_one')
    user_two = models.ForeignKey(User, related_name='friend_two')

    class Meta:
        unique_together = ('user_one', 'user_two')


