from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from transac.forms import UserForm, UploadForm, ShareForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
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

def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()

    return render_to_response(
        'transac/register.html', {'user_form': user_form, 'registered': registered}, context)

def index(request):
    context = RequestContext(request)
    curuser = request.user
    uploaded_docs = Transaction.objects.filter(uploader=curuser)
    return render_to_response('transac/index.html', {'uploaded_docs': uploaded_docs}, context)

@login_required
def upload(request):
    context = RequestContext(request)
    curuser = request.user
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            dat = upload_form.cleaned_data
            contype = str(dat['pdfdoc'])[-3:]
            if contype == 'pdf':
              t = upload_form.save(commit=False)
              t.uploader = curuser
              t.save()
            else:
              return HttpResponse("Only PDF documents supported!")
            return index(request)
        else:
            print upload_form.errors
    else:
        upload_form = UploadForm()
    return render_to_response('transac/upload.html', {'upload_form': upload_form}, context)


@login_required
def viewshared(request):
    context = RequestContext(request)
    curuser = request.user
    docs = TransactionView.objects.filter(viewer=curuser)
    return render_to_response('transac/viewshared.html', {'docs': docs}, context)


@login_required
def sharedoc(request):
    context = RequestContext(request)
    curuser = request.user.id
    if request.method == 'POST':
        share_form = ShareForm(curuser, request.POST)
        if share_form.is_valid():
            dat = share_form.cleaned_data
            tv = TransactionView(trans=dat['documents'], shared_by=curuser, viewer=dat['users'])
            tv.save()
            return manageshared(request)
        else:
            print share_form.errors
    else:
        share_form = ShareForm(curuser)
    return render_to_response('transac/sharedoc.html', {'share_form': share_form}, context)


@login_required
def manageshared(request):
    context = RequestContext(request)
    curuser = request.user.id
    docs = TransactionView.objects.filter(shared_by=curuser)
    return render_to_response('transac/manageshared.html', {'docs': docs}, context)


@login_required
def transactionview_delete(request, pk, template_name='transac/transactionview_confirm_delete.html'):
    transacview = get_object_or_404(TransactionView, pk=pk)
    if request.method=='POST':
        transacview.delete()
        return redirect('manageshared')
    return render(request, template_name, {'object':transacview})






















