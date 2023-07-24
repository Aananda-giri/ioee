from django.test import TestCase

# Create your tests here.



"""
# filter code whose title is 'test' and body is 'test'
Code.objects.filter(title='test')
Code.objects.filter(title__contains='test', code__contains='test')


# filter code whose title and body are same
from django.db.models import F
Code.objects.filter(title__exact=models.F('code')).delete()

# delete code whose body is null or empty string
from code_share.models import Code
from django.db.models import Q

Code.objects.filter(Q(code__isnull=True) | Q(code__exact='')).delete()

"""