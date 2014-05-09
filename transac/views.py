from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from transac.models import Transaction, TransactionView

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/transac/')
            else:
                return HttpResponse("Your account has been disabled!")
        else:
            print "Invalid login credentials: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied")
    else:
        return render_to_response('transac/login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/transac/')

@login_required
def index(request):
    context = RequestContext(request)
    current_user = request.user
    files_list = Transaction.objects.filter(uploader=current_user.id)
    view_list = TransactionView.objects.filter(viewer=current_user.id)
    context_dict = { 'files_list': files_list, 'view_list': view_list }
    response = render_to_response('transac/index.html', context_dict, context)
    return response
