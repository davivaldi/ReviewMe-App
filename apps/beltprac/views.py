from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User, Book, Review, Author
from django.contrib.auth.decorators import login_required

def index(request):

    return render(request, "beltprac/index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    print("here arre errors --> ", errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        print(request.method)
        name = request.POST['name']
        alias= request.POST['alias']
        email = request.POST['email']
        hashedPW = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
        newUser = User.objects.create(name=name, alias=alias, email=email, password=hashedPW)
        request.session['alias'] = request.POST['alias']
        request.session['userid'] = newUser.id
        print(newUser.id)
        messages.success(request, "Entry success")
        return redirect(f'/books')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['loginEmail'])
        if bcrypt.checkpw(request.POST['loginPassword'].encode(), user.password.encode()):
            request.session['alias'] = user.alias
            request.session['userid'] = user.id
            print("password match")
            return redirect('/books')
        else:
            print("failed password")
        return redirect('/')

@login_required(login_url='/')
def home(request):
    amazonBox = {
        "all_the_reviews": Review.objects.all(),
        "books": Book.objects.all()

    }

    return render(request, "beltprac/home.html", amazonBox)

def addReview(request):
    amazonBox = {
        "all_the_authors" : Author.objects.all()

    }

    return render(request, "beltprac/bookadd.html", amazonBox)

def bookAdded(request):
    if request.method =="POST":
        if request.POST['author'] == '':
            newAuthor = Author.objects.get(id=request.POST['dropdown'])
        else :
            newAuthor = Author.objects.create(name=request.POST['author'])      
        title = request.POST['title']
        print(title)
        desc = request.POST['desc']
        print(desc)
        rating = request.POST['rating']
        user  = User.objects.get(id=request.session['userid'])
        newBook = Book.objects.create(title=title,user=user,author=newAuthor)
        newReview = Review.objects.create(desc=desc,user=user,book=newBook,rating=rating)
        request.session['bookid'] = newBook.id

        print("this is the new id number -->",newBook.id)
    
    return redirect(f'/books/{newBook.id}')


def bookAdded1(request):
    if request.method =="POST":
        desc = request.POST['desc']
        print(desc)
        rating = request.POST['rating']
        book = Book.objects.get(id=request.session['bookid'])
        user  = User.objects.get(id=request.session['userid'])
        newReview = Review.objects.create(desc=desc,user=user,book=book,rating=rating)
        reviewedBook = Book.objects.get(id=request.session['bookid'])
        print("this is the new id number -->",reviewedBook)
        
    return redirect(f'/books/{reviewedBook}')
    

def singleBookHome(request, val):
    print("this is the id number", val)
    amazonBox = {
        "book" : Book.objects.get(id=val),
        "all_the_reviews": Review.objects.filter(id=val)

    }
    return render(request, "beltprac/bookreview.html",amazonBox)
    

def singleUserHome(request, val):
    print("this is the id number of the user", val)
    amazonBox = {
        "thisUser" : User.objects.get(id=val),
        "all_the_reviews" : Review.objects.filter(user=User.objects.get(id=val))
    }

    return render(request, "beltprac/userreview.html",amazonBox)
def logout(request):
    print("CLEAR SESSIOn")
    request.session.clear()
    return redirect('/')