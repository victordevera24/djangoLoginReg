from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages 
from models import *  
import bcrypt


def index(request):
    return render(request, ('login/index.html'))


def process(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    if request.method == 'POST':
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        request.session['name'] = request.POST['first_name']
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hash1)       

    return redirect('/success')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    if request.method == 'POST':
        u = User.objects.get(email=request.POST['email'])
        request.session['name'] = u.first_name
        return redirect ('/success')



def success(request):
    return render(request, ('login/success.html'))