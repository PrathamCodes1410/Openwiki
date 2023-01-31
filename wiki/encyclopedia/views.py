from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout
import markdown2
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse, HttpResponseRedirect


from .models import User, Author
from . import util


def home(request):
    return render(request, "encyclopedia/home.html", {
        "entries": util.list_entries()
    })

def index(request):
    return render(request, "encyclopedia/index.html")

def login(request):
    return render(request, "encyclopedia/login.html")


def register(request):
    return render(request, "encyclopedia/register.html")


def login_auth(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        # Check if authentication successful
        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "encyclopedia/login.html")


def register_auth(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "encyclopedia/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "encyclopedia/register.html", {
                "message": "Username already taken."
            })
        login(request)
        return render(request, "encyclopedia/login.html", {
            "s_message": "Account Successfully Created"
        })

    else:
        return render(request, "encycloepedia/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def convert(title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def display(request, title):
    f_writer = Author.objects.get(title = title)
    page = convert(title)
    if page == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": page,
            "author" : f_writer,
        })


def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert(entry_search)

        if html_content is not None:
            return render(request, "encyclopedia/page.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            result = []
            for entry in util.list_entries():
                if entry_search.lower() in entry.lower():
                    result.append(entry)

            return render(request, "encyclopedia/result.html", {
                "entries": result
            })


def new(request):
    if request.user.is_authenticated == False:
        return render(request, "encyclopedia/login.html", {
            "message": "Please login to your account to create page"
        })
    else:
        return render(request, "encyclopedia/create.html")


def save(request):
    if request.method == "POST":
        s_title = request.POST['title']
        s_content = request.POST['content']
        s_writer = request.POST['writer']

        for titles in util.list_entries():
            if s_title == titles:
                return render(request, "encyclopedia/NewError.html")

        util.save_entry(s_title, s_content)

        f_writer = User.objects.get(username = s_writer)

        entry = Author(
            title=s_title,
            d_writer=f_writer,
        )

        entry.save()

        return render(request, "encyclopedia/home.html", {
            "entries": util.list_entries()
        })


def edit(request):
    if request.user.is_authenticated == False:
        return render(request, "encyclopedia/login.html", {
            "message": "Please login to your account to edit"
        })
    else:
        if request.method == "POST":
            s_title = request.POST['e_title']
            s_content = util.get_entry(s_title)
            current_user = request.POST['e_user']
            s_author = request.POST['e_author']
            if current_user == s_author:
                return render(request, "encyclopedia/edit.html", {
                "edit_title": s_title,
                "edit_content": s_content,
            })
            else:
                return render(request, "encyclopedia/notauthorized.html")


def save_edit(request):
    if request.method == "POST":
        s_title = request.POST['title']
        s_content = request.POST['content']

        util.save_entry(s_title, s_content)

        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })



def random(request):
    import random

    list = util.list_entries()

    rand_title = random.choice(list)


    page = convert(rand_title)
    return render(request, "encyclopedia/page.html", {
        "title": rand_title,
        "content": page
    })
