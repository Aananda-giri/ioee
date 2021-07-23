from django.db import models

# Create your models here.

import datetime
from django.utils import timezone
#from user.models import User

# python3 manage.py makemigrations person
# python3 manage.py migrate --database=postgres
# python3 manaeg.py migrate --fake
from django.contrib.postgres.fields import ArrayField

## python3 manage.py migrate --database=horornot
class Person(models.Model):
    id = models.AutoField(primary_key=True)
    section_code = models.IntegerField(default=3030) 
    ioe_roll_no = models.CharField(max_length=12)
    
    views = models.PositiveIntegerField(default=0)
    votes = models.PositiveIntegerField(default=0)
    '''
    r1_votes = models.PositiveIntegerField(default=0)
    r1_views = models.PositiveIntegerField(default=0)
    
    r2_votes = models.PositiveIntegerField(default=0) 
    r2_views = models.PositiveIntegerField(default=0)
    
    r3_votes = models.PositiveIntegerField(default=0) 
    r3_views = models.PositiveIntegerField(default=0)'''
    
    gender_choices = [
        ('m', 'male'),
        ('f', 'female'),
    ]
    
    gender = models.CharField(
    max_length = 1,
    choices=gender_choices,
    default = '',
    )
    
    image_format = models.CharField(max_length=5)
    ioe_roll_no_with_format = models.CharField(max_length=18)
    url_base = 'https://exam.ioe.edu.np/Images/StudentCurrentImage/3030/'
    
    url = models.CharField(max_length=100, default=None, null=True)
    collage = models.CharField(max_length=3, default=None, null=True)
    faculty = models.CharField(max_length=5, default=None, null=True)
    year = models.SmallIntegerField(null=True)
    
    
    def __str__(self):
        return(self.url_base+self.ioe_roll_no+'.'+self.ioe_roll_no_with_format)

## python3 manage.py migrate --database=horornot
class RoundFemale(models.Model):
    id=models.AutoField(primary_key = True)
    
    ranked_ids = ArrayField(models.PositiveIntegerField(default=None),null=True, default=None)
    unranked_ids = ArrayField(models.PositiveIntegerField(default=None),null=True, default=None)
    
    voted_people_of_level = ArrayField(models.PositiveIntegerField(default=None), null=True, default=None)
    
    total_people_of_level = ArrayField(models.PositiveIntegerField(default=None), null=True, default=None)

    
    random_pairs = ArrayField(models.PositiveIntegerField(default=None), null=True, default=None)

## python3 manage.py migrate --database=horornot
class RoundMale(models.Model):
    id=models.AutoField(primary_key = True)
    
    ranked_ids = ArrayField(models.PositiveIntegerField(default=None),null=True, default=None)
    
    unranked_ids = ArrayField(models.PositiveIntegerField(default=None),null=True, default=None)

    total_people_of_level = ArrayField(models.PositiveIntegerField(default=None), null=True, default=None)
    
    voted_people_of_level = ArrayField(models.PositiveIntegerField(default=None), null=True, default=None)
    
    random_pairs = ArrayField(models.PositiveIntegerField(default=None), null=True, default=None)




#python3 manage.py migrate --database=hotornot
class Feedbacks(models.Model):
    username = models.CharField(max_length=50, default = None, null=True)
    body = models.CharField(max_length=500, default = None)
    loves = models.IntegerField(default=0)    
    email = models.EmailField(default = None,)
    
    pub_date = models.DateTimeField('date published',default=timezone.now)
    def __str__(self):
        return('Username: {}, Body:{}, email:{}'.format(self.username, self.body, self.email))
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        






'''
import os
f=os.listdir('/home/intelligence/Music/Website/img_lab/image_downloader_multiprocessing_python-master/pickle/female')
print('Before:',len(f))
f.remove('maybe_female')
print('After:',len(f))
m=os.listdir('/home/intelligence/Music/Website/img_lab/image_downloader_multiprocessing_python-master/pickle/male')


print('Before:',len(f))
m.remove('maybe_male')
print('Before:',len(m))

def progress(current, total, ioe_rollno='', barlength=65):
    percent = (current/total)*100
    hastrik = '#' * int(percent/100 * barlength)
    dash = '-' * int( barlength - len(hastrik) )
    print(str([hastrik + dash]) + str(current) + '  ' + str(int(percent)) + '%' + ' \t{}'.format(ioe_rollno),end='\r')
    
max=len(f)
from hotornot.models import Person
for pos,mm in enumerate(f):
    Person.objects.using('hotornot').create(id=pos, section_code=3030,ioe_roll_no=mm.replace('.'+mm.split('.')[1],''), gender='f', image_format=mm.replace(mm.split('.')[0]+'.',''), ioe_roll_no_with_format = mm, votes=0, views=0, collage=mm[:3], faculty=mm[6:9] )
    progress(pos,max)

max=len(m)
for pos,mm in enumerate(m):
    Person.objects.using('hotornot').create(id=pos+1450, section_code=3030,ioe_roll_no=mm.replace('.'+mm.split('.')[1],''), gender='m', image_format=mm.replace(mm.split('.')[0]+'.',''), ioe_roll_no_with_format = mm, votes=0, views=0, collage=mm[:3], faculty=mm[6:9] )
    progress(pos,max)

    
    
    
    
    
    
    
    
################ For refining collages data ##################
    
collages=[]
faculties=[]
students=[]

for n,collage in enumerate(max_students.keys()):
    if collage not in collages:collages.append(collage)
    
    for faculty in max_students[collage].keys():
        try:
            faculties[n].append(faculty)
        except:
            faculties.append([faculty])
        
        try:
           students[n].append(max_students[collage][faculty]) 
        except:
            students.append([max_students[collage][faculty]])
        
students = [[192, 96, 48, 48, 48, 48, 48], [144, 48, 48, 48, 48, 48, 48], [144, 48, 48, 48, 48, 48, 48], [96, 96, 48, 48, 48, 96, 48], [96, 96, 96, 48, 48], [96, 96, 96], [48, 48, 48], [96, 96, 96, 48], [96, 48, 48, 48], [96, 48, 48, 48], [48, 48], [96, 48, 48], [96, 48, 48], [96, 48, 48], [24]]

collages = ['PUL', 'THA', 'PAS', 'PUR', 'KAT', 'KAN', 'SEC', 'ACE', 'HCE', 'NCE', 'LEC', 'KIC', 'JAN', 'KEC', 'CHI']

faculties = [['BCE', 'BCT', 'BEI', 'BEL', 'BAR', 'BCH', 'BME'], ['BCE', 'BCT', 'BEI', 'BAR', 'BME', 'BIE', 'BAM'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAM', 'BME', 'BGE'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAR', 'BME', 'BAG'], ['BCE', 'BCT', 'BEI', 'BEL', 'BAR'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI', 'BEL'], ['BCE', 'BCT', 'BEI', 'BAR'], ['BCE', 'BCT', 'BEI', 'BEL'], ['BCE', 'BCT'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEI'], ['BCE', 'BCT', 'BEL'], ['BAR']]    '''
