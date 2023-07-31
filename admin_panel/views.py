from django.http import HttpRequest
from django.shortcuts import render


# Create your views here.
def all_in(request: HttpRequest):
    return render(request, 'admin_panel/articles/articles_list.html')
