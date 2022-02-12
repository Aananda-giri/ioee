import random, string
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


def get_random(size=6, chars= string.ascii_letters + string.digits + '_'):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_alphanumeric(size=6):
    random_val = get_random()
    fail_count=0
    if len(Person.objects.using('fuse_attend').filter(auto_pseudoid=random_val)) == 0:
        return random_val
    else:
        fail_count+=1
        #if count > 50:
        #    size += 1      #Implemant Later
        random_val = generate_random_alphanumeric()
        return random_val

#default/unseen data storage model
class IoeNoti(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length = 500, default=None, null=True, db_index=True)
    url = models.CharField(max_length=500, default=None, null=True, db_index=True)
    date = models.CharField(max_length=35, default=None, null=True)
    
    #dob_bs = NepaliDateField(default='2058-12-28')
    dob_ad = models.DateField(default=None, null=True)
    #dob = models.DateField(default=None, null=True)
    
    # sent list to each notification
    sent = ArrayField(models.CharField( max_length=6, blank=True), default=None, null=True)
    #delivered = BooleanField(default=True)
    
    def __str__(self):
        details = { 'title' : self.title, 'url' : self.url, 'date' : self.date }
        return str(details)
    
    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['title'], name='title'),
        ]



