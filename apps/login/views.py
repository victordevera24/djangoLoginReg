from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages 
from models import *  
import bcrypt
from django.db.models import Q


def index(request):
    request.session.clear()
    return render(request, ('login/index.html'))


def process(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            request.session['name'] = request.POST['first_name']
            User.objects.create(first_name=request.POST['first_name'], username=request.POST['username'], password=hash1, date_hired=request.POST['date_hired'])       
            u = User.objects.get(username=request.POST['username'])
            request.session['id'] = u.id
            return redirect('/dashboard')


def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            u = User.objects.get(username=request.POST['username'])
            request.session['id'] = u.id
            request.session['name'] = u.first_name
            return redirect ('/dashboard')



def success(request):
    if 'id' not in request.session:
        return redirect('/')
    else:
        wishlist = Item.objects.filter(wished_users=request.session['id'])
        items = Item.objects.filter(~Q(wished_users=request.session['id']))
        return render(request, ('login/success.html'), {'wishlist' : wishlist, 'items' : items} )


def add(request):
    if 'id' not in request.session:
        return redirect('/')
    return render(request, ('login/add.html'))


def addItem(request):
    if request.method == 'POST':
        errors = Item.objects.item_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/add')
        else:
            I = Item(item_name=request.POST['item_name'], adder = User.objects.get(id=request.POST['adder']))
            I.save()
            this_item = Item.objects.get(item_name = request.POST['item_name'])
            this_user = User.objects.get(id = request.session['id'])
            this_user.wished_items.add(this_item)
            return redirect('/dashboard')



def show(request, id):
    context = {
        'item' : Item.objects.get(id =id),
        'user' : User.objects.filter(wished_items = id)
    }
    return render(request, ('login/show.html'), context)



def addWish(request, id):
        this_item = Item.objects.get(id = id)
        this_user = User.objects.get(id = request.session['id'])
        this_user.wished_items.add(this_item)
        return redirect(('/dashboard'), { 'items' : Item.objects.all()} )


def remove(request, id):
    this_item = Item.objects.get(id = id)
    this_user = User.objects.get (id = request.session['id'])
    this_user.wished_items.remove(this_item)
    return redirect(('/dashboard'), { 'items' : Item.objects.all()} )


def delete(request, id):
    d = Item.objects.get(id=id)
    d.delete()
    return redirect(('/dashboard'), { 'items' : Item.objects.all()} )