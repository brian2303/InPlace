from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.forms import model_to_dict
from crum import get_current_request
from InPlace.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):    
    image = models.ImageField(upload_to='image_users', null=True, blank=True)
    email = models.EmailField('email address', unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass


class Group(models.Model):

    def toJSON(self):
        item = model_to_dict(self)
        return item


# class User(AbstractUser):
    # email = models.EmailField('email address', unique=True)
    # image = models.ImageField(upload_to='image_users', null=True, blank=True)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
