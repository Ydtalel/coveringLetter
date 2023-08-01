from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm, UserLogin, CoverLetterForm
from .models import CoverLetter, ProcessedCoverLetter
import os
from dotenv import load_dotenv
import openai
import json
import logging

load_dotenv()

# Здесь нужно указать ваш ключ API GPT-3.5 Turbo от OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
logging.basicConfig(filename='gpt3_processing_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def process_text(text):
    # Задайте параметры для вызова API GPT-3.5 Turbo
    prompt = f"Пожалуйста, улучшите следующий текст: \"{text}\". Улучшите его несколько раз и предоставьте варианты." \
             f" Текст должен быть составлен на русском языке."

    n = 5  # Количество требуемых улучшенных вариантов

    try:
        # Вызовите API GPT-3.5 Turbo для обработки текста
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text + "\nКонец"}  # Добавляем разделитель "Конец"
            ],
            n=n,
            max_tokens=400,
            stop="Конец",  # Используем "Конец" как стоп-слово для разделения ответов
            temperature=0.7,
        )

        # Извлекаем улучшенные варианты текста из ответа API
        improved_variants_list = [message["message"]["content"] for message in response["choices"]]

        # Удаляем разделитель "Конец" из каждого улучшенного варианта
        improved_variants_list = [variant.replace("Конец", "").strip() for variant in improved_variants_list]

        # Ограничиваем каждый улучшенный вариант до 300 символов
        improved_variants_list = [variant for variant in improved_variants_list]

        return improved_variants_list

    except Exception as e:
        # Если произошла ошибка, записываем ее в лог
        logging.error(f"Error processing text: {text}\nError details: {e}")
        return []


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

            # Сохранение текста в поле 'text' модели 'CoverLetter'
            cover_letter = CoverLetter.objects.create(user=request.user, text=text)

            # Отправка текста на обработку с помощью GPT-3.5 Turbo
            response = process_text(text)

            # Сохранение полученных вариантов ответа в базе данных
            for variant in response:
                ProcessedCoverLetter.objects.create(cover_letter=cover_letter, processed_text=variant)

            # Сохранение ответа от GPT-3.5 Turbo в файл response.json
            with open('response.json', 'w', encoding='utf-8') as file:
                json.dump(response, file, ensure_ascii=False, indent=4)

            return redirect('profile')
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
