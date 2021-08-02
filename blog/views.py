from django.shortcuts import render, HttpResponseRedirect
from .forms import LoginForm, SignUpForm, PostForm, changepassform
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import blogPost
from django.contrib.auth.models import Group


# Create your views here.

# Home
def home(request):
    posts = blogPost.objects.all()
    return render(request, 'home.html', {'posts':posts})

# About
def about(request):
    return render(request, 'about.html')

# contact
def contact(request):
    return render(request, 'contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = blogPost.objects.all()
        user = request.user
        full_name = user.get_full_name
        grp = user.groups.all()
        return render(request, 'dashboard.html', {'posts':posts, 'fullname':full_name, 'groups':grp})
    else:
        return HttpResponseRedirect('/login/')

# signup
def user_signup(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            user = fm.save()
            messages.success(request, 'Congratulation!! SignUp successfully')
            group = Group.objects.get(name='author')
            user.groups.add(group)
            return render(request, 'signup.html', {'form':fm})
    else:
        fm = SignUpForm()
    return render(request, 'signup.html', {'form':fm})

# user_login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successfully')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
        

# user_logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Add Post
def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                Bpost = blogPost(title=title,desc=desc)
                Bpost.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Update Post
def updatepost(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = blogPost.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post Updated successfully')
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = blogPost.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Delete Post
def deletepost(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = blogPost.objects.get(pk=id)
            pi.delete()
            messages.success(request, 'Post Deleted successfully')
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

# For Change Password with old password.
def chngpass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = changepassform(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request, 'Password Change Successfully...')
                return HttpResponseRedirect('/dashboard/')
        else:
            fm = changepassform(user=request.user)
        return render(request, 'chngpassword.html', {'form':fm})
    else:
        return HttpResponseRedirect('/login/')
   

