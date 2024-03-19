from django.shortcuts import render,HttpResponseRedirect

# Create your views here.

def index(request):
    context='a'
    return render(request,context=context)