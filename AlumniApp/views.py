from django.core.checks.messages import Error
from django.http import request
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate,login, logout
from datetime import date 
# Create your views here.

def index(request):
    return render(request,'index.html')

def user_login(request):
    error=""
    if request.method=='POST':
        u=request.POST['uname']
        p=request.POST['pwd']
        user=authenticate(username=u,password=p)
        if user:
            try:
                user1=StudentUser.objects.get(user=user)
                if user1.type=="student":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d={'error':error}
    return render(request,'user_login.html',d)

def user_signup(request):
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        i=request.FILES['image']
        p=request.POST['pwd']
        e=request.POST['email']
        con=request.POST['contact']
        gen=request.POST['gender']
        rollno=request.POST['rollno']
        branch=request.POST['branch']
        batchyear=request.POST['batchyear']
        description=request.POST['description']
        linkedinId=request.POST['linkedinId']
        try:
            user=User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            StudentUser.objects.create(user=user, mobile=con,image=i,gender=gen,type="student",
            rollno=rollno,batchyear=batchyear,description=description,branch=branch,linkedinId=linkedinId)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'user_signup.html',d)

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user=request.user
    student=StudentUser.objects.get(user=user)
    print(user)
    error=""
    if request.method=='POST':
        f=request.POST['fname']
        l=request.POST['lname']
        con=request.POST['contact']
        gen=request.POST['gender']
        student.user.first_name=f
        student.user.last_name=l
        student.mobile=con
        student.gender=gen
        try:
            student.save()
            student.user.save()
            error="no"
        except:
            error="yes"
        try:
            i=request.FILES['image']
            student.image=i
            student.save()
            error="no"
        except:
            pass
    d={'error':error,'student':student}
    return render(request,'user_home.html',d)

def Logout(request):
    logout(request)
    return redirect('index')

def blog_view(request):
    posts = Post.objects.all()
    photos=[]
    for p in posts:
        photos.append(PostImage.objects.filter(post=p).first())
    return render(request, 'blog.html', {'data':zip(posts,photos)})

def detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    photos = PostImage.objects.filter(post=post)
    return render(request, 'detail.html', {
        'post':post,
        'photos':photos
    })

def create_post_view(request):
    if request.method == 'POST':
        length = request.POST.get('length')
        title = request.POST.get('title')
        description = request.POST.get('description')

        post = Post.objects.create(
            title=title,
            description=description
        )        
        for file_num in range(0, int(length)):
            PostImage.objects.create(
                post=post,
                images=request.FILES.get(f'images{file_num}')
            )
    return render(request, 'create-post.html')

def know_your_family(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    data = StudentUser.objects.all()
    if request.method == 'POST':
        branch=request.POST['branch']
        batchyear=request.POST['batchyear']
        print(branch)
        print(batchyear)
        if branch and batchyear:
            data = StudentUser.objects.filter(branch=branch,batchyear=batchyear)
        elif not branch and batchyear:
            data = StudentUser.objects.filter(batchyear=batchyear)
        elif branch and not batchyear:
            data = StudentUser.objects.filter(branch=branch)
    d = {'data':data}
    return render(request,"know_your_family.html",d)

def job_openings(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    data=Job.objects.all()
    d={'data':data}
    return render(request,'job_openings.html',d)

def photo_gallery(request):
    return render(request,'photo_gallery.html')

def create_job_post(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=='POST':
        company=request.POST['company']
        role=request.POST['role']
        eligibility=request.POST['eligibility']
        location=request.POST['location']
        applylink=request.POST['applylink']        
        description=request.POST['description']
        user=request.user
        studentuser=StudentUser.objects.get(user=user)
        try:
            Job.objects.create(user=studentuser,company=company,role=role,
            eligibility=eligibility,description=description,location=location,applylink=applylink)
            error="no"
        except:
            error="yes"
    d={'error':error}
    return render(request,'create_job_post.html',d)

def apply_for_referral(request,pid):
    if request.method=='POST':
        resume=request.FILES['resume']
        description=request.POST['description']
        print(resume)
        print(description)
        alumni=StudentUser.objects.get(id=pid)
        print(alumni)
        print(request.user.first_name)
        try:
            Referral.objects.create(user=request.user,
            alumni=alumni,resume=resume,description=description,applydate=date.today())
            return render(request,'know_your_family.html')
        except:
            print("Error")
    return render(request,'apply_for_referral.html')

def handle_referral(request):
    referrals=Referral.objects.all()
    data={}
    data['referrals']=referrals
    return render(request,'handle_referral.html',data)
