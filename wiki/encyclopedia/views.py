import django
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, name):
    if util.get_entry(name) == None:
        return render(request, "encyclopedia/invalid.html")
    title = name
    content = markdown2.markdown(util.get_entry(name))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

def search(request):
    if request.method == "POST":
        query = request.POST.get("q")
        results = []
        if util.get_entry(query) is not None:
            return redirect("entry", query)
        for entry in util.list_entries():
            if query in entry:
                results.append(entry)
        return render(request, "encyclopedia/results.html", {
            "query": query,
            "results": results,
        })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        for entry in util.list_entries():
            if title == entry:
                return render(request, "encyclopedia/createInvalid.html")
        util.save_entry(title, content)
        return redirect("entry", title)
    else:
        return render(request, "encyclopedia/create.html")
    
def edit(request, title):
    if request.method == "POST":
        newContent = request.POST.get("content")
        if util.get_entry(title) == None:
            return render(request, "encyclopedia/editInvalid.html")
        util.save_entry(title, newContent)
        return redirect("entry", title)    
    else:
        if util.get_entry(title) == None:
            return render(request, "encyclopedia/editInvalid.html")
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "oldContent": util.get_entry(title),
        })