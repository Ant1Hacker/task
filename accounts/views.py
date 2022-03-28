from django.contrib.auth import login as _login, logout as _logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
import weasyprint

from accounts.forms import UserRegisterForm, UserLoginForm, UserEditForm, LinkForm, EducationAndEmploymentHistoryForm
from accounts.models import Link, EducationAndEmploymentHistory


@login_required(login_url='/login')
def home(request):
    user = request.user
    return render(request, 'accounts/home.html', {"user": user})


def login(request):
    form = UserLoginForm()

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                _login(request, user)
                return redirect(home)

    return render(request, 'accounts/login.html', {
        'form': form
    })


@login_required
def links(request, pk):
    link = get_object_or_404(Link, user=request.user, pk=pk)
    form = LinkForm(instance=link)
    if request.method == 'POST':
        form = LinkForm(instance=link, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(edit)
    return render(request,
                  'accounts/link.html',
                  {'form': form, 'link': link})


@login_required
def link_add(request):
    form = LinkForm()
    if request.method == 'POST':
        form = LinkForm(data=request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect(edit)
    return render(request,
                  'accounts/add_link.html',
                  {'form': form})


@login_required
def link_remove(request, pk):
    link = get_object_or_404(Link, user=request.user, pk=pk)
    link.delete()
    return redirect(edit)


@login_required
def statuses(request, pk):
    status = get_object_or_404(EducationAndEmploymentHistory, user=request.user, pk=pk)
    form = EducationAndEmploymentHistoryForm(instance=status)
    if request.method == 'POST':
        form = EducationAndEmploymentHistoryForm(instance=status, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(edit)
    return render(request,
                  'accounts/status.html',
                  {'form': form, 'status': status})


@login_required
def status_add(request):
    form = EducationAndEmploymentHistoryForm()
    if request.method == 'POST':
        form = EducationAndEmploymentHistoryForm(data=request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.user = request.user
            status.save()
            return redirect(edit)
    return render(request,
                  'accounts/add_status.html',
                  {'form': form})


@login_required
def status_remove(request, pk):
    status = get_object_or_404(EducationAndEmploymentHistory, user=request.user, pk=pk)
    status.delete()
    return redirect(edit)


@login_required
def edit(request):
    links = Link.objects.filter(user=request.user)
    status = EducationAndEmploymentHistory.objects.filter(user=request.user)
    if request.method == 'POST':
        form = UserEditForm(instance=request.user,
                            data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(home)
    else:
        form = UserEditForm(instance=request.user)
    return render(request,
                  'accounts/edit.html',
                  {'form': form, 'links': links, 'status': status})


@login_required
def logout(request):
    _logout(request)
    return redirect(login)


def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(login)
    return render(request, 'accounts/register.html', {
        'form': form
    })


@login_required
def user_pdf(request):
    """
    sudo apt-get install libpangocairo-1.0-0
    """
    user = request.user
    html = render_to_string('accounts/pdf.html',
                            {'user': user})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename={user.username}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('staticfiles/pdf.css')])
    return response
