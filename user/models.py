from django.db import models

# Create your models here.
class Usermodel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    phoneno = models.IntegerField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "usermodel"

class advertisementmodel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=1024, blank=True, null=True)
    addcat = models.TextField(max_length=1024, blank=True, null=True)
    post_url = models.TextField(max_length=1024, blank=True, null=True)
    image = models.ImageField(upload_to='add_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'advertisementmodel'

class productmodel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    image = models.ImageField(upload_to='product_image/', blank=True, null=True)
    addcat = models.TextField()
    desc = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "productmodel"

class UserSearchHistory(models.Model):
    user = models.ForeignKey(Usermodel, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    cdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_search_history"
        ordering = ['-cdate']