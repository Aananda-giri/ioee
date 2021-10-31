from django.db import models

# Create your models here.

import datetime
#from dateutil.relativedelta import relativedelta
import uuid

from django.utils import timezone
#from nepali_datetime_field.models import NepaliDateField

#from user.models import User

# python3 manage.py makemigrations person
# python3 manage.py migrate --database=brainmap
# python3 manaeg.py migrate --fake



from django.contrib.postgres.fields import ArrayField
class Person(models.Model):
    #id = models.AutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ioe_roll_no = models.CharField(max_length = 30, default=None, null=True, db_index=True)
    profile_pic = models.FileField(upload_to='person/static/person/images')
    
    nick_name = models.CharField(max_length = 30, default='')
    first_name = models.CharField(max_length = 30)#, db_index=True)
    
    middle_name = models.CharField(max_length = 30, db_index=True)
    
    last_name = models.CharField(max_length = 30, db_index=True)
    
    #dobb_bs = NepaliDateField()
    dob_ad = models.DateField(default=None, null=True)
    dob = models.DateField(default=None, null=True)
    
    profession = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True, db_index=True)
    #models.CharField(max_length = 30)
    
    personality =  models.CharField(max_length = 30)
    sources = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)
    post_box = models.IntegerField(default=None, null=True)
    permanent_address = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)
    uses = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)
    social_engineering = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)
    
    gender_choices = [
        ('m', 'male'),
        ('f', 'female'),
        ('l', 'female'),
        ('g', 'female'),
        ('o', 'other')
    ]
    
    gender = models.CharField(
    max_length = 1,
    choices=gender_choices,
    default = '',
    )
    

    

    
    
    
    fathers_name = models.CharField(max_length = 100, default=None,  null=True)
    mothers_name = models.CharField(max_length = 100, default=None,  null=True)
    
    location = ArrayField(models.CharField(max_length=100, blank=True), default=None, null=True)
    
    phone_number = ArrayField(models.BigIntegerField(default=None, blank=True), default=None, null=True, db_index=True)
    #phone_number = models.BigIntegerField(default=0,)
    
    emails = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True, db_index=True)
    
    social_media_profiles = ArrayField(models.CharField(max_length=300, blank=True), default=None, null=True)
    adress = ArrayField(models.CharField(max_length=300, blank=True), default=None, null=True)
    '''[0] - liknedin
       [2] - twitter
       [2] - instagram
       [3] - tiktok
       [4] - discord
       [5] - snapchat
       [6] - facebook
       [7] - pinterest
       [8] - youtube
       [9] - reddit
       [10] - quora
       [11] - viber
       [12] - whatsapp
       [13] - wechat
       [14] - tumbler
       [15] - qq
       [16] - qzone
       [17] - SocialBee
       [18] - 
       
    '''
    likes = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True, db_index=True)
    
    dislikes = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True, db_index=True)
    
    religion = models.CharField(max_length = 25, db_index=True)
    
    country = models.CharField(max_length = 25, db_index=True)
    
    hobbies = ArrayField(models.CharField(max_length=150, blank=True), default=None, null=True)

    family_members = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)#Foreign key to their username

    education = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)
    
    smoke = models.BooleanField(default=None, null=True)
    
    drink = models.BooleanField(default=None, null=True)
    
    rating = models.IntegerField(default=False)
    
    personal_details = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)
    
    tags = ArrayField(models.CharField(max_length=50, blank=True), default=None, null=True)
    
    symbols = ArrayField(models.CharField(max_length=50, blank=True), default=None, null=True)
    #models.CharField(max_length = 30, default='')
    
    profile_pic= ArrayField(models.CharField(max_length=500, blank=True), default=None, null=True)
    #models.CharField(max_length = 300, default='')
    
    pub_date = models.DateTimeField('date published',default=timezone.now)
    def __str__(self):
        details = {'first_name' : self.first_name, 'middle_name' : self.middle_name, 'last_name' : self.last_name, 'gender' : self.gender, 'profession' : self.profession, 'likes' : self.likes, 'dislikes' : self.dislikes, 'religion' : self.religion, 'country' : self.country, 'hobbies' : self.hobbies, 'family_members' : self.family_members, 'education' : self.education, 'smoke' : self.smoke, 'drink' : self.drink, 'rating' : self.rating, 'tags' : self.tags, 'social_media_profiles':self.social_media_profiles, 'profile_pic':self.profile_pic }
        return str(details)
    
    
    #first_name = models.CharField(max_length=100)
    #last_name = models.CharField(max_length=100)
    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
        ]



















'''

likes = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)

dislikes = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)

p.religion = 'hindu'

p.country = 'nepal'

hobbies = ArrayField(models.CharField(max_length=150, blank=True), default=None, null=True)

p.family_members = ['samrid','krshna','devpriya']

p.education = 'Greenland High School'

p.smoke = False

p.drink = False

p.rating = 8

p.tags = ['mild narcissism']
p.tags.append('drama queen')
'''

'''Driver
    Expressive
    Amiable
    Analytical
    openness
    agreeableness
    extraversion
    neuroticism
    Extraverted Thinking.
    Introverted Thinking.
    Extraverted Feeling.
    Introverted Feeling.
    Extraverted Sensation.
    Introverted Sensation.
    Extraverted Intuition.
    Introverted Intuition.
    sensetive'''

'''




<Person: {'first_name': 'Dakshina', 'middle_name': '', 'last_name': 'shrestha', 'gender': 'f', 'profession': ['Chief of Academics and Associate Professor at Sagarmatha Engineering College', 'Program Leader at Sagarmatha National College'], 'likes': None, 'dislikes': None, 'religion': 'hindu', 'country': 'nepal', 'hobbies': None, 'family_members': None, 'education': ['Siddhartha Vanasthali Institute', "Saint Xavier's College", 'Bangladesh University of Engineering and Technology (BUET)'], 'smoke': False, 'drink': False, 'rating': 10, 'tags': ['heroine', 'strict'], 'social_media_profiles': ['https://www.linkedin.com/in/dakshina-shrestha-1ba9669/', '', '', '', '', '', 'https://www.facebook.com/dakshina.shrestha.3', '', '', '', '', '', '', '', '', '', '', '', ''], 'profile_pic': ['http://snc.edu.np/wp-content/uploads/2016/02/1475480031pic-WS-Copy-340x360.jpg', 'http://sagarmatha.edu.np/images/dakshina_shrestha.png', 'https://theedunepal.ap-south-1.linodeobjects.com/bachelorfairuploads/clients/sagarmathaeng/teams/Dakshina_Shrestha_1610694587.png', 'http://sagarmatha.edu.np/uploads/content_image/8.png', 'http://sagarmatha.edu.np/images/dakshina_shrestha.png']}>




''

import os
from person.models import Person
Person.objects.using('brainmap').filter(profession='teacher')

'''
