from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    return render(request, 'app/index.html')



def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error="yes"
        except:
            error="yes"
    d = {'error': error}
    return render(request, 'app/admin_login.html', d)

def user_login(request):
    error=""
    if request.method == 'POST':
       u = request.POST['uname'];
       p = request.POST['pwd'];
       user = authenticate(username=u, password=p)
       if user:
            try:
               user1 = SUser.objects.get(user=user)
               if user1.type == "seeker":
                   login(request, user)
                   error="no"
               else:
                   error="yes"
            except:
               error="yes"
       else:
            error="yes"
    d = {'error': error}
    return render(request, 'app/user_login.html', d)

def recruiter_login(request):
    error=""
    if request.method == 'POST':
       u = request.POST['uname'];
       p = request.POST['pwd'];
       user = authenticate(username=u, password=p)
       if user:
            try:
               user1 = Recruiter.objects.get(user=user)
               if user1.type == "recruiter" and user1.status!="pending":
                   login(request, user)
                   error="no"
               else:
                   error="not"
            except:
               error="yes"
       else:
            error="yes"
    d = {'error': error}
    return render(request, 'app/recruiter_login.html', d)


def recruiter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        company = request.POST['company']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Recruiter.objects.create(user=user, mobile=con, image=i, gender=gen, company=company, type="recruiter", status="pending")
            error="no"
        except:
            error="yes"
    d = {'error': error}
    return render(request, 'app/recruiter_signup.html')

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request, 'app/user_home.html')

def Logout(request):
    logout(request)
    return redirect('index')

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'app/admin_home.html')

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    return render(request, 'app/recruiter_home.html')


def user_signup(request):
    error = ""
    if request.method == "POST":
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            SUser.objects.create(user=user, mobile=con, image=i, gender=gen, type="seeker")
            error="no"
        except:
            error="yes"
    d = {'error': error}
    return render(request, 'app/user_signup.html',d)


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = SUser.objects.all()
    d = {'data': data}
    return render(request, 'app/view_users.html', d)


def delete_user(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    seeker = SUser.objects.get(id=pid)
    seeker.delete()
    return redirect('view_users')


from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Update the session so the user doesn't get logged out after the password change
            update_session_auth_hash(request, form.user)
            return redirect('user_home')  # Redirect to user_home after successful password change
        else:
            return render(request, 'app/change_password.html', {'form': form, 'error': 'yes'})
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'app/change_password.html', {'form': form})


