FROM python:3.11-slim

#создание работочей директории
WORKDIR /app 

#установка зависимостей
ENV PYTHONUNBUFFERED=1

#копирование файла с зависимостями в контейнер
COPY requirements.txt .

#обонвление пип и установка зависимостей из файла requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

#копирование всех файлов из текущей директории в контейнер
COPY . .

#команда для запуска бота при старте контейнера
CMD ["python", "bot_2.py"]