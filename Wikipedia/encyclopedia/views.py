from django.shortcuts import render,redirect
from markdown2 import Markdown

from . import util

import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })



def title(request,title):
    if request.method == "GET":
       if util.get_entry(title):
          content = util.get_entry(title)
          converted = util.md_to_html(content)
          return render(request,"encyclopedia/title.html",{
            "title": converted, "name": title
          })
       else:
           return render(request,"encyclopedia/notfound.html", {
               "name" : title
           })
    else:
        return render(request,"encyclopedia/notfound.html",{
            "name": title
        })



def search(request):
    if request.method == "POST":
        title = request.POST.get('q')
        entries = util.list_entries()
        if title:
                for i in entries:
                    if title.lower() in i.lower():
                       return redirect('title', title=i)
                else:
                     return render(request,"encyclopedia/notfound.html",{
                      "name" : title
                     })
        else:
           return render(request,"encyclopedia/notfound.html",{
            "name" : title
        })
    else:
        return render(request,"encyclopedia/notfound.html",{
            "name" : "error"
        })



def add(request):
        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            entries = util.list_entries()
            if title not in entries:
                util.save_entry(title, content)
                return render(request,"encyclopedia/title.html",{
                   "title": util.get_entry(title), "name": title
                })
            else:
                return render(request,"encyclopedia/error.html",{
                    "name" : title
                })
        else:
            return render(request,"encyclopedia/addnew.html")



def edit(request,title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title,content)
        return redirect('title', title=title)
    else:
        title1 = util.get_entry(title)
        return render(request,"encyclopedia/edit.html",{
            "title" : title1, "name" : title
        })

    

def rand(request):
    entries = util.list_entries()
    picked_entry = random.choice(entries)
    return redirect('title', title=picked_entry)