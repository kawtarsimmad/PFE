from django.shortcuts import render
from . models import Category
# Create your views here.
def category(request):
    return render(request, 'categories/category.html')
def categories(request):
    return render(request, 'categories/categories.html',{'ct':Category.objects.all()})
