FROM python:3.12-slim

# Чтобы pip не кешировал пакеты и логи будут без задержек
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY . .

# Открываем порт (для uvicorn)
EXPOSE 3000

# Значение по умолчанию (все равно переопределим в compose)
CMD ["uvicorn", "tests.frontend.fastapi_main:app", "--host", "0.0.0.0", "--port", "3000"]
