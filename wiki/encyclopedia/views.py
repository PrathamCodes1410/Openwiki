from django.shortcuts import render

import markdown2


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert(title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def display(request, title):
    page = convert(title)
    if page == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/page.html", {
            "title": title,
            "content": page
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
    return render(request, "encyclopedia/create.html")


def save(request):
    if request.method == "POST":
        s_title = request.POST['title']
        s_content = request.POST['content']

        for titles in util.list_entries():
            if s_title == titles:
                return render(request, "encyclopedia/NewError.html")

        util.save_entry(s_title, s_content)

        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def edit(request):
    if request.method == "POST":
        s_title = request.POST['e_title']
        s_content = util.get_entry(s_title)

    return render(request, "encyclopedia/edit.html", {
        "edit_title": s_title,
        "edit_content": s_content,
    })


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
