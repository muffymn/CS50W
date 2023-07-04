from django.shortcuts import render
import markdown
import random

from . import util

def convert_md(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html_content = convert_md(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            all = util.list_entries()
            similar = []
            for entry in all:
                if entry_search.lower() in entry.lower():
                    similar.append(entry)
            return render(request, "encyclopedia/search.html", {
                "similar": similar
            })

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        add_title = request.POST['title']
        add_content = request.POST['content']
        exists = util.get_entry(add_title)
        if exists is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry already exists"
            })
        else:
            util.save_entry(add_title, add_content)
            html_content = convert_md(add_title)
            return render(request, "encyclopedia/entry.html", {
                "title": add_title,
                "content": html_content
            })

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
def random_entry(request):
    all = util.list_entries()
    random_entry = random.choice(all)
    html_content = convert_md(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })

    