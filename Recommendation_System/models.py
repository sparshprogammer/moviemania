from django.db import models

from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator,MinValueValidator
import datetime
from friendship.signals import (
    friendship_request_created, friendship_request_rejected,
    friendship_request_canceled,
    friendship_request_viewed, friendship_request_accepted,
    friendship_removed, follower_created, follower_removed,
    followee_created, followee_removed, following_created, following_removed
)


# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # The additional attributes we wish to inclu1de.
    #user_id = models.(primary_key=False)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    date_of_birth = models.DateField(blank=True)

    def __unicode__(self):
        return self.user.username

class Friendship(models.Model):
    from_friend = models.ForeignKey(
        User, related_name = 'friend_set'
    )
    to_friend = models.ForeignKey(
        User,related_name='to_friend_set'
    )
    def __str__(self):
        return '%s, %s' %(self.from_friend.username,
                        self.to_friend.username)
    class Admin:
        pass
    class Meta:
        unique_together = (('to_friend','from_friend'), )

class Friendship_Request(models.Model):
    request_from_friend = models.ForeignKey(
        User, related_name='request_friend_set'
    )
    request_to_friend = models.ForeignKey(
        User,default=None, related_name='request_to_friend_set'
    )
    friendship_status = models.IntegerField(blank=False,default=0)
    action_user = models.IntegerField(blank=False)
    def __str__(self):
        return '%s, %s' %(self.request_from_friend.username,
                        self.request_to_friend.username)

    class Meta:
        unique_together = (('request_to_friend','request_from_friend'),('request_from_friend','request_to_friend'), )

class Status_update(models.Model):
    posted_to = models.ForeignKey(settings.AUTH_USER_MODEL,default=1,related_name='Posted_to')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='Posted_by')
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=500)
    def __unicode__(self):
        return self.status

class Movie(models.Model):
    title = models.CharField(max_length=200,blank=False)
    year= models.PositiveIntegerField(blank=False)
    director=models.CharField(blank=True,max_length=200)
    writer=models.CharField(blank=True,max_length=200)
    star_cast= models.CharField(blank=True,max_length=200)
    imdb_ratings = models.FloatField(validators=[MaxValueValidator(10),MinValueValidator(1)])
    genres = models.CharField(max_length=200,blank=False)
    summary = models.TextField(blank=True)
    length = models.PositiveIntegerField(blank=False)
    movie_img = models.ImageField(upload_to='movies_img',blank=True)
    img = models.URLField(blank=True)
    def get_absolute_url(self):
        return reverse('detail',kwargs={'pk':self.pk})
    def __str__(self):
        return self.title
class Rating(models.Model):
    movies= models.ForeignKey(Movie, default=1, blank=False)
    rate = models.FloatField()
    user = models.ForeignKey(User)
    class Meta:
        unique_together = ('movies','user')
class Like(models.Model):
    like_status = models.ForeignKey(Status_update,blank=False)
    liked_by = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
class Comment(models.Model):
    comment_status = models.ForeignKey(Status_update,blank=False)
    commented_by = models.ForeignKey(User)
    comment = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)