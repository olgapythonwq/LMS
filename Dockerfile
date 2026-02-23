# Используем официальный slim-образ Python 3.13
FROM python:3.13-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Копируем файлы зависимостей в контейнер
COPY requirements.txt ./
COPY requirements-dev.txt ./

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt && pip install -r requirements-dev.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000
