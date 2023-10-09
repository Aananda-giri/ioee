# code_share/models.py
# database: 'fuse_attend'
# python3 manage.py migrate --database=fuse_attend
from django.db import models
from django.utils import timezone
import uuid
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from .functions import DriveFunctions



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

# class File(models.Model):
#     author = models.CharField(max_length=25, blank=True)
#     title = models.CharField(max_length=255, blank=True)
#     description = models.TextField(max_length=500, blank=True)
#     drive_links = ArrayField(
#         models.URLField(blank=True, null=True)
#     )
#     created_on = models.DateTimeField(default=timezone.now)
    


#     def __str__(self):
#         return str(self.drive_links)
    
#     def delete(self, *args, **kwargs):
#         print(f'class after list: {list(self.drive_links)}')
        
#         # delete files from drive
#         DriveFunctions().delete_files(list(self.drive_links))

#         super().delete(*args, **kwargs)


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

'''
class Comment(models.Model):
    post = models.ForeignKey(
        Code, on_delete = models.CASCADE, related_name='comments', to_field='id'
        )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
'''

"""    
    #def image_tag(self):
    #    if self.image.url is not None:
    #        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    #    else:
    #        return """


# ------------------
# New model Format
# ------------------

from django.db import models, transaction

class Container(models.Model):
    unique_uuid = models.UUIDField(
        unique=True,primary_key=True, default=uuid.uuid4, db_index=True
        )
    
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=80, default='anonymous')
    author_email = models.EmailField(default='')
    created_on = models.DateField()
    # To hide the code from home page and search

    is_private = models.BooleanField(default=False) # hide the private code from home_page
    
    tags = ArrayField(models.CharField(
        max_length=150, blank=True),
        default=list,
        null=True
        )
    likes_count = models.PositiveIntegerField(default=0)

    author_ip = models.CharField(max_length=25, default='')
    
    created_on = models.DateTimeField(auto_now_add=True)
    
    stars_ip = ArrayField(models.CharField(
        max_length=25, blank=True), default=None, null=True)
    
    valid_email = models.BooleanField(default=True) # False if the email is valid (i.e. could not send the mail)
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title
    
    def get_public(self):
        return Codes.objects.filter(private_code=False)
    
    def get_absolute_url(self):
        if self.private_code==False:
            return f'/code/{self.id}/'
    

    @classmethod
    @transaction.atomic
    def create_container_file_code(cls, container_data=None, file_data=None, code_data=None):
        print(f'file_data:{file_data}\n code_data:{code_data}\n container_data:{container_data}')
        # Dummy data
        # container_data = {
        #     'title': 'Container 1',
        #     'author': 'John Doe',
        #     # 'created_on': '2023-07-08',
        #     # 'unique_uuid': '123e4567-e89b-12d3-a456-426614174000',
        #     'tags': ['tag1, tag2, tag3'],
        #     # 'likes_count': 10
        # }

        # file_data = [
        #     {'link': 'https://example.com/file1', 'type': 'text', 'filename': 'file1.txt'},
        #     {'link': 'https://example.com/file2', 'type': 'img', 'filename': 'file2.txt'},
        #     {'link': 'https://example.com/file3', 'type': 'other', 'filename': 'file3.txt'}
        # ]

        # code_data = [
        #     {'body': 'print("Hello, World!")'},
        #     {'body': 'x = 10\ny = 20\nz = x + y'}
        # ]

        # Create Container instance
        container = cls.objects.create(**container_data)

        # Create File instances related to the Container
        if file_data != None:
            files = [Files(container=container, **file_item) for file_item in file_data]
            Files.objects.bulk_create(files)

        if code_data != None:
            # Create Code instances related to the Container
            codes = [Codes(container=container, **code_item) for code_item in code_data]
            Codes.objects.bulk_create(codes)

        return container
    
    @classmethod
    @transaction.atomic
    def bulk_create_files(cls, container_id, file_data_list):
        # Get the Container object with the given ID
        try:
            container = cls.objects.get(unique_uuid=container_id)
        except Container.DoesNotExist:
            # Handle the case when the Container with the given ID doesn't exist
            return

        # Create a list of Files objects to be bulk created
        files_to_create = [Files(container=container, **file_data) for file_data in file_data_list]
        # files_to_create = [Files(container=container, filename='1',type='img', link= file_data) for file_data in file_data_list]

        # Perform the bulk creation
        Files.objects.bulk_create(files_to_create)
        return file_data_list
        '''
            file_data_list = [
                {'file_name': 'file1.txt', 'file_type': 'text'},
                {'file_name': 'file2.png', 'file_type': 'image'},
                # Add more file data dictionaries as needed
            ]

            container_id = 1  # Replace with the ID of the specific Container you want to associate the Files with

            bulk_create_files_for_container(container_id, file_data_list)

        '''

    @classmethod
    @transaction.atomic
    def add_one_code(cls, container_uuid, filename='code', body=''):
        # Get the Container object with the given ID
        try:
            container_instance = cls.objects.get(unique_uuid=container_uuid)
        except Container.DoesNotExist:
            # Handle the case when the Container with the given ID doesn't exist
            return
        # Create a new instance of Codes
        new_code = Codes(container=container_instance, filename=filename, body=body)

        # Save the new code instance to the database
        new_code.save()

        return {'filename': filename, 'body': body, 'unique_uuid': container_uuid}
    
class Files(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='files')
    FILE_TYPE_CHOICES = (
        ('text', 'Text'),
        ('img', 'Image'),
        ('other', 'Other'),
    )
    '''
        remove: link, download_link :: use file_id only
        link:           https://drive.google.com/file/d/1WoSOw86YZMGvL9QP1er65Igm72_QCG3P/view?usp=drivesdk
        download_link:  https://drive.usercontent.google.com/download?id=1WoSOw86YZMGvL9QP1er65Igm72_QCG3P&export=download&confirm=t
        file_id:        1WoSOw86YZMGvL9QP1er65Igm72_QCG3P
        iframe:         <iframe src="https://drive.google.com/file/d/1WoSOw86YZMGvL9QP1er65Igm72_QCG3P/preview" width="640" height="480" allow="autoplay"></iframe>
    '''
    link = models.URLField()
    download_link = models.URLField(default='')
    google_drive_file_id = models.CharField(max_length=50, default='')
    
    type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    filename = models.CharField(max_length=255, default='')
    def __str__(self):
        return f'<{self.type}> <{self.filename}> <{self.link}>'

    def delete(self, *args, **kwargs):
        print(f'class after list: {str(self.link)}')
        
        # delete files from drive
        DriveFunctions().delete_files(str(self.link))
        
        # delete file
        super().delete(*args, **kwargs)

        # Delete container if it has no other associated files or codes
        if self.container.files.count() == 0 and self.container.codes.count() == 0:
            self.container.delete()
    

class Codes(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE, related_name='codes')    # model.cascade deletes code on deleting container
    filename = models.CharField(default='code', max_length=25)
    body = models.TextField(max_length=1000)

    def __str__(self):
        return self.body
    
    def delete(self, *args, **kwargs):
        # delete code
        super().delete(*args, **kwargs)

        # Delete container if it has no other associated files or codes
        if self.container.files.count() == 0 and self.container.codes.count() == 0:
            self.container.delete()    
    
    
'''
# Creating new container with two files and two codes
from django.utils import timezone
from .models import Container, File, Code

# Create a new Container instance
container = Container.objects.create(
    title='New Container',
    author='John Doe',
    date_of_creation=timezone.now(),
    unique_uuid='your-unique-uuid',
    tags='tag1, tag2',
    likes_count=0
)

# Create two File instances associated with the container
file1 = File.objects.create(
    container=container,
    link='http://example.com/file1',
    type='text'
)

file2 = File.objects.create(
    container=container,
    link='http://example.com/file2',
    type='img'
)

# Create two Code instances associated with the container
code1 = Code.objects.create(
    container=container,
    body='print("Code 1")'
)

code2 = Code.objects.create(
    container=container,
    body='print("Code 2")'
)


# -----------------------
# Bulk Create Files
# -----------------------

# from .models import File

# Assuming you have a list of file data to create
file_data = [
    {'link': 'https://example.com/file1', 'type': 'text'},
    {'link': 'https://example.com/file2', 'type': 'img'},
    {'link': 'https://example.com/file3', 'type': 'other'},
    # ... add more file data as needed
]

# Create File instances using bulk_create()
file_instances = [File(link=data['link'], type=data['type']) for data in file_data]
File.objects.bulk_create(file_instances)


# ----------------------
# Create Simulatneously
# ----------------------
from django.db import transaction
from .models import Container, File, Code

@transaction.atomic
def create_container_file_code(container_data, file_data, code_data):
    # Create Container instance
    container = Container.objects.create(**container_data)

    # Create File instances related to the Container
    files = [File(container=container, **file_item) for file_item in file_data]
    File.objects.bulk_create(files)

    # Create Code instances related to the Container
    codes = [Code(container=container, **code_item) for code_item in code_data]
    Code.objects.bulk_create(codes)

    return container

    
# -----------------------------
# Example using transactions.
# -----------------------------
from django.db import transaction
from .models import Container, File, Code

@transaction.atomic
def create_container_file_code():
    # Dummy data
    container_data = {
        'title': 'Container 1',
        'author': 'John Doe',
        'date_of_creation': '2023-07-08',
        'unique_uuid': '123e4567-e89b-12d3-a456-426614174000',
        'tags': 'tag1, tag2, tag3',
        'likes_count': 10
    }

    file_data = [
        {'link': 'https://example.com/file1', 'type': 'text'},
        {'link': 'https://example.com/file2', 'type': 'img'},
        {'link': 'https://example.com/file3', 'type': 'other'}
    ]

    code_data = [
        {'body': 'print("Hello, World!")'},
        {'body': 'x = 10\ny = 20\nz = x + y'}
    ]

    # Create Container instance
    container = Container.objects.create(**container_data)

    # Create File instances related to the Container
    files = [File(container=container, **file_item) for file_item in file_data]
    File.objects.bulk_create(files)

    # Create Code instances related to the Container
    codes = [Code(container=container, **code_item) for code_item in code_data]
    Code.objects.bulk_create(codes)

    return container
'''