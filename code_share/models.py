#database: 'fuse_attend'
from django.db import models
from django.utils import timezone
import uuid
from django.contrib.postgres.fields import ArrayField

# settings.configure()


class Code(models.Model):
    #id = models.AutoField(primary_key=True)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    code = models.TextField()
    author = models.CharField(max_length=80, default='')
    email = models.EmailField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='')
    tags = ArrayField(models.CharField(
        max_length=150, blank=True), default=None, null=True)

    # False if the email is valid (i.e. could not send the mail)
    valid_email = models.BooleanField(default=True)
    # To hide the code from home page and search
    hide_code = models.BooleanField(default=False)
    stars=models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Code {} by {}'.format(self.code, self.author)
# branch of code
class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    Parent = models.ForeignKey(Code, on_delete=models.CASCADE)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    code = models.TextField()
    author = models.CharField(max_length=80, default='')
    email = models.EmailField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='')
    branch_name = models.CharField(max_length=20, default='')
    tags = ArrayField(models.CharField(
        max_length=150, blank=True), default=None, null=True)

    # False if the email is valid (i.e. could not send the mail)
    valid_email = models.BooleanField(default=True)
    # To hide the code from home page and search
    hide_code = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on'] #to order based on created_date

    def __str__(self):
        return 'Code {} by {}'.format(self.code, self.author)
###########################################
# Unused models
###########################################
class Post(models.Model):
    post = models.CharField(max_length=50, default=None, null=True)
    body = models.CharField(max_length=500, default=None)
    loves = models.IntegerField(default=0)
    email = models.EmailField(default=None,)

    pub_date = models.DateTimeField('date published', default=timezone.now)

    def __str__(self):
        return('post: {}'.format(self.post))

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

# from code_share.models import Code, CodeBranch
# Code.objects.using('fuse_attend').all()[0].valid_email
# Code.objects.using('fuse_attend').all()[0].hide_code

# Code.objects.using('fuse_attend').filter(author='anon').delete()
# Code.objects.using('fuse_attend').filter(author='A').delete()
# Code.objects.using('fuse_attend').filter(author='Jdkdkend').delete()
# Code.objects.using('fuse_attend').filter(author='Hmm').delete()
