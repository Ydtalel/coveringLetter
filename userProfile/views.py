from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import RegisterForm, UserLogin, CoverLetterForm
from .models import CoverLetter


def user_profile(request):
    user = request.user

    try:
        cover_letter = CoverLetter.objects.get(user=user)
    except CoverLetter.DoesNotExist:
        cover_letter = None

    context = {
        'user': user,
        'cover_letter': cover_letter,
    }
    return render(request, 'userProfile/profile.html', context)

def generate_cover_letter(request):
    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            # Ваша логика обработки формы может быть здесь
            pass
    else:
        form = CoverLetterForm()

    context = {
        'form': form,
    }
    return render(request, 'userProfile/cover_letter_form.html', context)


def home(request):
    return render(request, 'userProfile/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')

    else:
        form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'userProfile/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = UserLogin()
    context = {
        'form': form,
    }

    return render(request, 'userProfile/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')
