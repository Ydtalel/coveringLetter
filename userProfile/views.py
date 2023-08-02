from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, UserLogin, CoverLetterForm

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CoverLetter, ProcessedCoverLetter
from .serializers import CoverLetterSerializer, ProcessedCoverLetterSerializer
from OpenAI import process_text, GPTProcessingError, ERROR_MESSAGES
from django.contrib import messages
import logging

import requests.exceptions
from urllib3.exceptions import TimeoutError


class CoverLetterViewSet(viewsets.ModelViewSet):
    queryset = CoverLetter.objects.all()
    serializer_class = CoverLetterSerializer

    @action(detail=True, methods=['get'])
    def processed_letters(self, request, pk=None):
        cover_letter = self.get_object()
        processed_letters = cover_letter.processed_letters.all()
        serializer = ProcessedCoverLetterSerializer(processed_letters, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


class ProcessedCoverLetterViewSet(viewsets.ModelViewSet):
    queryset = ProcessedCoverLetter.objects.all()
    serializer_class = ProcessedCoverLetterSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()


def user_profile(request):
    user = request.user

    # Получаем все объекты CoverLetter пользователя, если они есть
    cover_letters = CoverLetter.objects.filter(user=user)

    context = {
        'user': user,
        'cover_letters': cover_letters,  # Передаем QuerySet с объектами CoverLetter
    }
    return render(request, 'userProfile/profile.html', context)


@login_required
def generate_cover_letter(request):
    if request.method == 'POST':
        form = CoverLetterForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']

            try:
                # Сохранение текста в поле 'text' модели 'CoverLetter'
                cover_letter = form.save(commit=False)  # Сохранение формы без фактической записи в базу данных
                cover_letter.user = request.user
                cover_letter.save()

                response = process_text(text)

                # Проверка на наличие ошибки в ответе
                if 'error' in response:
                    error_code = response['error']['code']

                    # Проверка, есть ли соответствующее сообщение об ошибке в словаре
                    if error_code in ERROR_MESSAGES:
                        error_message = ERROR_MESSAGES[error_code]
                    else:
                        error_message = "Произошла ошибка при обработке текста. Пожалуйста, попробуйте еще раз позже."

                    messages.error(request, error_message)



                # Сохранение полученных вариантов ответа в базе данных
                for variant in response:
                    ProcessedCoverLetter.objects.create(cover_letter=cover_letter, processed_text=variant)

            except GPTProcessingError as e:
                # Обработка ошибок, возникающих при обработке текста через GPT-3.5 Turbo
                error_message = str(e)
                messages.error(request, error_message)

            except (requests.exceptions.RequestException, TimeoutError) as e:
                # Обработка ошибок соединения или тайм-аута
                error_message = "Ошибка соединения или тайм-аута при обработке текста. Пожалуйста, попробуйте " \
                                "еще раз позже."
                logging.error(f"Connection or Timeout Error processing text: {text}\nError details: {e}")
                messages.error(request, error_message)

            except Exception as e:
                # Обработка других неожиданных ошибок
                error_message = "An unexpected error occurred. Please try again later."
                logging.error(f"Unexpected error processing text: {text}\nError details: {e}")
                messages.error(request, error_message)
            return redirect('profile')  # Перенаправление пользователя на страницу профиля
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
