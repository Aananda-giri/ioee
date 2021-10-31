from django.db import models

import datetime
from django.utils import timezone
from fernet_fields import EncryptedTextField
from django.db import IntegrityError

import random
import string

db=[]

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

class Person(models.Model):
    # add db_index=True if you plan to look objects up by it
    # blank=True is so you can validate objects before saving - the save method will ensure that it gets a value
    #id = models.AutoField(primary_key=True)
    auto_pseudoid = models.CharField(max_length=16, blank=True, editable=False, unique=True, db_index=True)
    
    
    username = EncryptedTextField(max_length=150)
    password = EncryptedTextField(max_length=150)
    
    #email = models.EmailField(default = None,)
    
    
    login_url = models.CharField(default = None, null=True, max_length = 500)
    collage = models.CharField(default = None, null=True, max_length = 100)
    level = models.CharField(default = None, null=True, max_length = 15)
    faculty = models.CharField(default = None, null=True, max_length = 30)
    section = models.CharField(default = None, null=True, max_length = 15)
    #roll_no = models.SmallIntegerField(default = 0)
    
    def save(self, *args, **kwargs):
        if not self.auto_pseudoid:
            self.auto_pseudoid = generate_random_alphanumeric(6)
            # using your function as above or anything else
        success = False
        failures = 0
        while not success:
            try:
                super(Person, self).save(*args, **kwargs)
            except IntegrityError:
                 failures += 1
                 if failures > 5: # or some other arbitrary cutoff point at which things are clearly wrong
                     raise
                 else:
                     # looks like a collision, try another random value
                     self.auto_pseudoid = generate_random_alphanumeric(16)
            else:
                 success = True

    def __str__(self):
        return('\tUsername: '+ self.username + '\n' + 'auto_pseudoid: \'' + self.auto_pseudoid +'\'')
