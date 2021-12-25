#database='brainmap'


# Create your models here.


#from dateutil.relativedelta import relativedelta
import uuid
import datetime
from django.db import models
from django.utils import timezone
from nepali_datetime_field.models import NepaliDateField

#from user.models import User

# python3 manage.py makemigrations person
# python3 manage.py migrate --database=brainmap
# python3 manaeg.py migrate --fake



from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User


#default/unseen data storage model
class Person(models.Model):
    #user having login credentials
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ioe_roll_no = models.CharField(max_length = 30, default=None, null=True, db_index=True, unique=True)
    
    # empty_profile => non_empty_profile=False
    non_empty_profile = models.BooleanField(default = False, db_index=True)
    nick_name = models.CharField(max_length = 30, default='')
    first_name = models.CharField(max_length = 30, default='', db_index=True)#, db_index=True)
    
    middle_name = models.CharField(max_length = 30, default='', db_index=True)
    
    last_name = models.CharField(max_length = 30, default='', db_index=True)
    
    dob_bs = NepaliDateField(default='2058-12-28')
    dob_ad = models.DateField(default=None, null=True)
    dob = models.DateField(default=None, null=True)
    
    profession = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True, db_index=True)
    
    personality =  models.CharField(max_length = 30, default='')
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
    
    phone_number = ArrayField(models.DecimalField(max_digits=10, decimal_places=0, default=0), default=None, null=True, db_index=True)
    email = models.EmailField(default='')
    emails = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True, db_index=True)
    
    adress = ArrayField(models.CharField(max_length=300, blank=True), default=None, null=True)
    
    likes = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True, db_index=True)
    
    dislikes = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True, db_index=True)
    
    religion = models.CharField(max_length = 25, db_index=True)
    
    country = models.CharField(max_length = 25, db_index=True)
    
    hobbies = ArrayField(models.CharField(max_length=150, blank=True), default=None, null=True)

    family_members = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)#Foreign key to their username

    education = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)
    
    smoke = models.BooleanField(default=None, null=True)
    
    drink = models.BooleanField(default=None, null=True)
    
    rating = models.IntegerField(default=10)
    
    symbols = ArrayField(models.CharField(max_length=50, blank=True), default=None, null=True)
    
    profile_pic= ArrayField(models.CharField(max_length=500, blank=True), default=None, null=True)
    
    last_edit_date = models.DateTimeField('date published',default=timezone.now)
    #pub_date = models.DateTimeField('date published',default=timezone.now)
    
    #profile_pic = models.FileField(upload_to='person/static/person/images')
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
    #personal_details = ArrayField(models.CharField(max_length=250, blank=True), default=None, null=True)
    #phone_number = models.BigIntegerField(default=0,)
    #social_media_profiles = ArrayField(models.CharField(max_length=300, blank=True), default=None, null=True)
    #tags = ArrayField(models.CharField(max_length=50, blank=True), default=None, null=True)

    
    def __str__(self):
        details = {'first_name' : self.first_name, 'middle_name' : self.middle_name, 'last_name' : self.last_name, 'gender' : self.gender, 'profession' : self.profession, 'dob_ad':self.dob_ad, 'likes' : self.likes, 'dislikes' : self.dislikes, 'religion' : self.religion, 'country' : self.country, 'hobbies' : self.hobbies, 'family_members' : self.family_members, 'education' : self.education, 'smoke' : self.smoke, 'rating' : self.rating, 'symbols':self.symbols, 'profile_pic':self.profile_pic }
        return str(details)
    #def get_section
    #males=FilterMale()
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




Person.objects.using('brainmap').create(first_name= 'Dakshina', middle_name= '', last_name= 'shrestha', gender= 'f', profession= ['Chief of Academics and Associate Professor at Sagarmatha Engineering College', 'Program Leader at Sagarmatha National College'], likes= None, dislikes= None, religion= 'hindu', country= 'nepal', hobbies= None, family_members= None, education= ['Siddhartha Vanasthali Institute', "Saint Xavier's College", 'Bangladesh University of Engineering and Technology (BUET)'], smoke= False, drink= False, rating= 10, tags= ['heroine', 'strict'], social_media_profiles= ['https://www.linkedin.com/in/dakshina-shrestha-1ba9669/', '', '', '', '', '', 'https://www.facebook.com/dakshina.shrestha.3', '', '', '', '', '', '', '', '', '', '', '', ''], profile_pic= ['http://snc.edu.np/wp-content/uploads/2016/02/1475480031pic-WS-Copy-340x360.jpg', 'http://sagarmatha.edu.np/images/dakshina_shrestha.png', 'https://theedunepal.ap-south-1.linodeobjects.com/bachelorfairuploads/clients/sagarmathaeng/teams/Dakshina_Shrestha_1610694587.png', 'http://sagarmatha.edu.np/uploads/content_image/8.png', 'http://sagarmatha.edu.np/images/dakshina_shrestha.png'])


p=[{'Personal Information:': {'First Name': 'PRAGATI', 'Middle Name': '', 'Last Name': 'BANIYA', 'Emailaddress': 'pragatibaniya62@gmail.com', 'Personal Contact Number': '9818879833', 'Dob': '2058-12-04', 'Gender': 'F', 'Father Name': 'HOM BAHADUR BANIYA'}, 'College Details:': {'College ': 'Sagarmatha Engineering College', 'College RollNo.': 'SEC076BCT028', 'Admission Date:': '9/17/2019'}, 'Faculty Details:': {'Field of Study:': 'Computer Engineering', 'Degree': 'Bachelor in Engineering'}, 'Local Guardian': {'Name': 'JYOTI  BASNET', 'Telephone': '', 'Address': 'KIRTIPUR'}},


{'Personal Information:': {'First Name': 'AASTHA', 'Middle Name': '', 'Last Name': 'GAUTAM', 'Emailaddress': 'rgnumberth79@gmail.com', 'Personal Contact Number': '9869063537', 'Dob': '2059-10-29', 'Gender': 'F', 'Father Name': 'RAMESH  GAUTAM'}, 'College Details:': {'College ': 'Sagarmatha Engineering College', 'College RollNo.': 'SEC076BCE002', 'Admission Date:': '9/9/2019'}, 'Faculty Details:': {'Field of Study:': 'Civil Engineering', 'Degree': 'Bachelor in Engineering'}, 'Local Guardian': {'Name': 'REKHA PAWAN GAUTAM', 'Telephone': '', 'Address': 'KIRTIPUR'}},





{'Personal Information:': {'First Name': 'SHOVA ', 'Middle Name': '', 'Last Name': 'WAGLE', 'Emailaddress': 'shovawagle000@gmail.com', 'Personal Contact Number': '9816626035', 'Dob': '2058-07-22', 'Gender': 'F', 'Father Name': ''}, 'College Details:': {'College ': 'Sagarmatha Engineering College', 'College RollNo.': 'SEC075BCE042', 'Admission Date:': '9/14/2018'}, 'Faculty Details:': {'Field of Study:': 'Civil Engineering', 'Degree': 'Bachelor in Engineering'}, 'Local Guardian': {'Name': '', 'Telephone': '', 'Address': ''}},


''

import os
from person.models import Person
Person.objects.using('brainmap').filter(profession='teacher')

'''

class Photos(models.Model):
    ioe_roll_no = models.CharField(max_length=12, primary_key=True)
    #year_code = models.IntegerField(default=None, null=True)
    urls = ArrayField(models.CharField(max_length=500, blank=True), default=None, null=True)

class SocialMedia(models.Model):
    id = models.AutoField(primary_key = True)
    profile_url = models.CharField(max_length=300, blank=True, default=None)
    
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.social_media_profile

    #pub_date = models.DateField()
    #class Meta:
    #    ordering = ['headline']

class Tags(models.Model):
    id = models.AutoField(primary_key = True)
    tag = models.CharField(max_length=300, blank=True, default=None)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return self.tag

#For adding custom new fields
class Name(models.Model):
    id = models.AutoField(primary_key = True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)#, default=Person.objects.using('brainmap').get(id='5e60dd01-fdf2-404e-8d9a-2211935f667d').id)# primary_key=True, to_field='id')
    
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=750, default='')
    def __str__(self):
        return "%s: %s" % self.name# ,self.value


'''class Value(models.Model):
    name = models.OneToOneField(
        Name,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    value = models.CharField(max_length=750)
    def __str__(self):
        return "%s" % self.value

#from person.models import Person
#>>> Person.objects.using('brainmap').create()'''

class test_model(models.Model):
    id = models.AutoField(primary_key = True)
    phone_num = models.DecimalField(max_digits=10, decimal_places=0, default=9999999999)
    name = models.CharField(max_length=10, default='')
    
    def set_price(self, price):
        self.price= price
    def set_name(self, name):
        self.name = name

#database=default
#additional data for django User model (***not_required**)
# default user fields: date_joined, email, first_name, groups, id, is_active, is_staff, is_superuser, last_login, last_name, logentry, password, user_permissions, userdata, username
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    is_verified = models.BooleanField(default = False, db_index=True)
    email = models.EmailField(default='')
    #college = models.CharField(max_length=30)
    #major = models.CharField(max_length=30)
