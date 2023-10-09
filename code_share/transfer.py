'''
# to run: 
`
from code_share.transfer import update_codes_version
update_codes_version()
`
'''
# -----------------------------------------------------------
# Migration oc Code model from old version to new version
# -----------------------------------------------------------
from code_share.models import Container, Code, Branch, Codes
def update_codes_version():
    codes = Code.objects.all()
    for code in codes:
        for branch in code.branch_set.all():
                print(f'branch: {branch.id} created')
        # Create a new Container instance
        container = Container.objects.create(
                title=code.title,
                author=code.author,
                author_email=code.email,
                created_on=code.created_on,
                unique_uuid=code.id,
                tags=code.tags,
                likes_count=code.stars,
                is_private=code.private_code,
                author_ip=code.author_ip,
                stars_ip=code.stars_ip,
                valid_email=code.valid_email

            )
        print(container.unique_uuid)
        if code.title:
            file_name = code.title
        else:
            file_name = 'file-name'
        
        if len(file_name) > 25:
            file_name = file_name[:25]

        # Create a new instance of Codes
        new_code = Codes(container=container, filename=file_name, body=code.code)

        # Save the new code instance to the database
        new_code.save()
        print(container.unique_uuid)
        
        if  code.branch_set.all():
            # code has no branch
            print(f'code: {code.id} has no branch')
            for branch in code.branch_set.all():
                if branch.title:
                    file_name = branch.title
                else:
                    file_name = 'file-name'
                
                if len(file_name) > 25:
                    file_name = file_name[:25]
                
                # create branch
                new_branch = Codes(container=container, filename=file_name, body=branch.code)
                new_branch.save()
                print(f'branch: {branch.id} created, file_name: {file_name}, code_sample: {branch.code[:10]}')

# delete all old codes
def delete_old_codes():
    codes = Code.objects.all()
    for code in codes:
        code.delete()
    print('all old codes deleted')

'''


class Code(models.Model):
    #id = models.AutoField(primary_key=True)
    code = models.TextField()
    

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
'''