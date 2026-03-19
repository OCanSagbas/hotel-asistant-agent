FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını güncelle
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Gerekli dosyaları kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Uygulama portunu dışarı aç
EXPOSE 7860

# Konteyner başlatıldığında uygulamayı çalıştır
CMD ["python", "app.py"]
