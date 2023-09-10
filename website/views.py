from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from.models import Record

def home(request):
    records = Record.objects.all()
    # IF THE PERSON IS LOGGING
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged in!!")
            return redirect("home")
        else:
            messages.error(request, "There was an ERROR. Please Try Again!!")
            return redirect("home")

    return render(request, "home.html", {"records":records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out!!!")
    return redirect("home")


def register_user(request):
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome to CRM!!!")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})
    return render(request, "register.html", {"form": form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record":customer_record})
    else:
        messages.error(request, "You must be Logged In to view that page!!!")
        return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, f'Record of "{delete_it.firstname} {delete_it.lastname}" is Deleted Successfully!!!')
        return redirect("home")
    else:
        messages.error(request, "You must be Logged In to Delete a Record!!!")
        return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=="POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, f'Record of "{add_record.firstname} {add_record.lastname}" is Added Successfully!!!')
                return redirect("home")
        return render(request, "add_record.html", {"form" : form})
    else:
        messages.error(request, "You must be Logged In!!!!")
        return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        current = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current)
        if form.is_valid():
            update=form.save()
            messages.success(request, f'Record of "{update.firstname} {update.lastname}" is Updated Successfully!!!')
            return redirect("home")
        return render(request, "update_record.html", {"form" : form})
    else:
        messages.error(request, "You must be Logged In!!!!")
        return redirect("home")
