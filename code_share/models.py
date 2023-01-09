# code_share/models.py
# database: 'fuse_attend'
# python3 manage.py migrate --database=fuse_attend
from django.db import models
from django.utils import timezone
import uuid
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# settings.configure()

# for snippet in all_codes:
#     Code.objects.using('ioee').create(id=snippet.id, code=snippet.code, author = snippet.author, author_ip=snippet.author_ip, email=snippet.email, created_on=snippet.created_on, title=snippet.title, tags=snippet.tags, stars_ip=snippet.stars_ip, valid_email=snippet.valid_email, private_code=snippet.private_code, stars=snippet.stars, output_photo=snippet.output_photo)
class Code(models.Model):
    #id = models.AutoField(primary_key=True)
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    code = models.TextField()
    author = models.CharField(max_length=80, default='')
    author_ip = models.CharField(max_length=25, default='')
    email = models.EmailField(default='')
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default='')
    tags = ArrayField(models.CharField(
        max_length=150, blank=True), default=None, null=True)
    stars_ip = ArrayField(models.CharField(
        max_length=25, blank=True), default=None, null=True)
    # False if the email is valid (i.e. could not send the mail)
    valid_email = models.BooleanField(default=True)
    # To hide the code from home page and search
    private_code = models.BooleanField(default=False) #hide the private code from home_page
    stars = models.PositiveIntegerField(default=0)
    
    # to upload output of a code as image
    # source : https://stackoverflow.com/a/35459441
    # output_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    #Branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='p_branch')
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Code {} by {}'.format(self.code, self.author)
    
    def get_absolute_url(self):
        if self.private_code==False:
            return f'/code/{self.id}/'
        
    def get_public_codes(self):
        return Code.objects.filter(private_code=False)

class Photo(models.Model):
    # to upload output of a code as image
    parent_code = models.ForeignKey(
        Code, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=70 , null=True)
    image = models.ImageField(upload_to='static/images/code_share/', null=True, blank=False)
    #description = models.TextField()
    
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    def __str__(self):
        return self.title

# branch of code
class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    Parent = models.ForeignKey(Code, on_delete=models.CASCADE, null=True)
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
    private_code = models.BooleanField(default=False)
    star = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['created_on'] #to order based on created_date

    def __str__(self):
        return 'Code {} by {}'.format(self.code, self.author)
###########################################
# Unused models
###########################################
# class Comment(models.Model):
#     post = models.ForeignKey(
#         Code, on_delete = models.CASCADE, related_name='comments')
#     body = models.CharField(max_length=500, default=None)
#     loves = models.IntegerField(default=0)
#     email = models.EmailField(default=None,)

#     pub_date = models.DateTimeField('date published', default=timezone.now)

#     def __str__(self):
#         return('post: {}'.format(self.post))

#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Comment(models.Model):
    post = models.ForeignKey(
        Code, on_delete = models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


"""    
    #def image_tag(self):
    #    if self.image.url is not None:
    #        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    #    else:
    #        return """

