# Официальный образ Python (slim версия для экономии места)
FROM python:3.10-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код
COPY . .

# Прокидываем порт, который использует Streamlit по умолчанию
EXPOSE 8501

# Проверка работоспособности сервиса
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Команда для запуска приложения
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
