from django.contrib import admin
from .models import *
# Register your models here.
class AdminJob(admin.ModelAdmin):
    list_display=['company','role']

class AdminStudentUser(admin.ModelAdmin):
    list_display=['user','batchyear']

class AdminReferral(admin.ModelAdmin):
    list_display=['alumni']
admin.site.register(StudentUser,AdminStudentUser)
admin.site.register(Job,AdminJob)
admin.site.register(Referral)
class PostImageAdmin(admin.StackedInline):
    model = PostImage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
       model = Post

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass