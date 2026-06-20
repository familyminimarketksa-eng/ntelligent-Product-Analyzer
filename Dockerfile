FROM python:3.10-slim

# প্রয়োজনীয় সিস্টেম ডিপেন্ডেন্সি ইনস্টল করা
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright এবং তার ভেতরের Chromium ব্রাউজার ইনস্টল করা
RUN playwright install --with-deps chromium

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]