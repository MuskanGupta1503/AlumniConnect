from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
import os

# Create your models here.
class StudentUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,null=True)
    image = models.FileField(null=True)
    gender = models.CharField(max_length=10,null=True)
    type = models.CharField(max_length=15,null=True)
    rollno = models.CharField(max_length=11,null=True)
    batchyear = models.IntegerField(null=True)
    description = models.CharField(max_length=500,null=True)
    branch = models.CharField(max_length=30,null=True)
    linkedinId = models.CharField(max_length=50,null=True)
    def _str_(self):
        return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'images/')

    def __str__(self):
        return self.post.title

    # def extension(self):
    #     name,extension=os.path.splitext(self.images.name)
    #     if extension=='mp4':
    #         return 'mp4'
    #     else:
    #         return 'other'

class Job(models.Model):
    user=models.ForeignKey(StudentUser,on_delete=models.CASCADE)
    company=models.CharField(max_length=30,null=True)
    role=models.CharField(max_length=50,null=True)
    eligibility = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=600,null=True)
    location = models.CharField(max_length=100,null=True)
    applylink = models.CharField(max_length=100,null=True)
    def _str_(self):
        return self.company+self.role
    
class Referral(models.Model):
    alumni=models.ForeignKey(StudentUser,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    resume = models.FileField(null=True)
    applydate = models.DateField()
    description=models.TextField()
    def _str_(self):
        return self.id 