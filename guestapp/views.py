from django.http import HttpResponse
from django.shortcuts import redirect, render

from guestapp.models import login, tbl_user

# Create your views here.
def guesthome(request):
    return render (request,'guest/index.html')

def loginhome(request):
    return render (request,'guest/login.html')

def login_process(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if login.objects.filter(
            username=username,
            password=password,
        
        ).exists():

            log = login.objects.get(
                username=username,
                password=password,
               
            )

            request.session['loginid'] = log.loginid
            usertype = log.usertype

            if usertype == 'admin':
                return redirect('/adminapp/adminindex')
            elif usertype == 'user':
                return redirect('/userapp/userhome')
        
            else:
                return HttpResponse(
                    "<script>alert('Request not accepted');window.location='/guestapp/login';</script>"
                )
        else:
            return HttpResponse(
                "<script>alert('Invalid credentials or account not approved');window.location='/guestapp/login';</script>"
            )

    return HttpResponse(
        "<script>alert('Invalid request');window.location='/guestapp/login';</script>"
    )
        
def registration(request):
    return render (request,'guest/registration.html')
def userreg_process(request):
    if request.method == "POST":
        lob = login()
        lob.username = request.POST.get("username")
        lob.password = request.POST.get("password")
        lob.usertype = "user"
       
        if login.objects.filter(username=request.POST.get("username")).exists():
            return HttpResponse("<script>alert('Already Exists..'); window.location='/Guest/officerreg';</script>")
        else:
            lob.save()

            tob = tbl_user()
            tob.username = request.POST.get("username")
            tob.email = request.POST.get("email")
            tob.loginid = lob
            tob.save()

            return HttpResponse("<script>alert('Successfully registered'); window.location='/Guest/officerreg';</script>")
