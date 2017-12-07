import uuid, os
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.contrib.auth import models as authModels

# Create your models here.
from django.db import models

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('books/img', filename)

def getProfilePath(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('profiles/img', filename)

def get_slug(instance, *argv):
    slug = ''
    for arg in argv:
        slug += slugify(arg)
    return slug


class Subscription(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    subscribed = models.BooleanField(default=True)

    def __str__(self):
        return self.email

class Pokemon(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    image = models.CharField(max_length=100, db_index=True)
    pokedex = models.IntegerField()
    type = models.CharField(max_length=30, db_index=True)
    summary = models.CharField(max_length=200, db_index=True)


    def __str__(self):
        return u'%s' % (self.name)

#Extending User model
class Profile(models.Model):
    user = models.OneToOneField(authModels.User)
    dob = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=getProfilePath, blank=True)
    favorites = models.ManyToManyField(Pokemon)
    
    def __str__(self):
        return 'Profile: {}'.format(self.user.username)



