# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import hashlib
 
#The Ribbit model has the attributes which include a CharField with maximum length of 140 characters to store the content, a ForeignKey to the User model (so that we have a relation between the two models) and a DateTimeField which is automatically populated with the time when the instance of the model is saved. 
class Ribbit(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now=True, blank=True)
 
#The UserProfile Model, we've a OneToOne field that defines a One to One relation with the User Model and a ManyToMany field to implement the follows/followed_by relation. The related_name parameter allows us to use the relation backwards using a name of our choice. We've also set symmetrical to False to ensure that if User A follows B then User B doesn't automatically follow A. We've also defined a function to get the link to the gravatar image based upon the user's url and a property to get (if the UserProfile exists for the user) or create one when we use the syntax <user_object>.profile. This allows us to fetch the properties of UserProfile quite easily.  
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
 
    def gravatar_url(self):
        return "http://www.gravatar.com/avatar/%s?s=50" % hashlib.md5(self.user.email).hexdigest()
 
 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

