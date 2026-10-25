# Стадия 1: Сборка и установка зависимостей
FROM python:3.11-slim AS builder

WORKDIR /app

# Обновляем pip
RUN pip install --no-cache-dir --upgrade pip

# Копируем файл зависимостей до остального кода для кэширования слоев
COPY requirements.txt .

# Устанавливаем зависимости в отдельную директорию
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Стадия 2: Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Копируем установленные зависимости из первой стадии
COPY --from=builder /install /usr/local

# Копируем исходный код приложения
COPY . .

# Открываем порт, на котором будет работать gunicorn
EXPOSE 5000

# Точка входа для запуска приложения через gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]