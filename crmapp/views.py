from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import Signupform,AddRecordForm
from .models import Records




# Create your views here.
def home(request):
    record = Records.objects.all()
    
    
    
    
    # check see if logging in 
    if request.method=="POST":
        username= request.POST['username']
        password= request.POST['password']
        #authenticate
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"You are login sucessfully")
            return redirect('home')
        else:
           messages.error(request,'There Was An Error Loggin In, Please Try Again..... ')
    return render(request, 'home.html', context={'record':record})
def login_user(request):
    context = {}
    return render(request, 'home.html', {})
def logout_user(request):
    logout(request)
    messages.success(request,"you are sucessfully logout ")
    return redirect('home')
    
def register_user(request):
    if request.method=="POST":
        form= Signupform(request.POST)
        if form.is_valid():
            form.save()
            # authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'you have sucessfully register')
            return redirect('home')
    else:
        form = Signupform()
        context = {'form':form}
        return render(request, 'register.html',context)

def customer_record(request,pk):
    if request.user.is_authenticated:
        # look up records
        cr = Records.objects.get(id=pk)
        return render(request,'record.html',{'cr':cr})
    else:
        messages.success(request,'you Must be login that page')
        return redirect('home')
    
 
 
 
 
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        dele = Records.objects.get(id=pk)
        dele.delete()
        messages.success(request,'Record Deleted Sucessfully')
        return redirect('home')
    else:
       messages.success(request,'you must be login to that')
       return redirect('home')
   
def add_user(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=="POST":
            if form.is_valid():
                adds= form.save()
                messages.success(request,"record add")
                return redirect('home')
        return render(request,'add.html',{'form':form})
    else:
        messages.success(request,"You must be login ")
        return redirect('home')


def update_record(request,pk):
    if request.user.is_authenticated:
        cr = Records.objects.get(id =pk)
        form = AddRecordForm(request.POST or None, instance=cr)
        if form.is_valid():
            form.save()
            messages.success(request,'You are sucessfully updated')
            return redirect('home')
        return render(request,'update.html',{'form':form,'cr':cr})
    else:   
        messages.success(request,"You must be login ")
        return redirect('home')
    

