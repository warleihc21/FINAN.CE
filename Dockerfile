FROM python:3.12-slim

# Instala dependências de sistema necessárias para o WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libjpeg-dev \
    libxml2 \
    libxslt1.1 \
    libpq-dev \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia o requirements.txt e instala os pacotes Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos da aplicação
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando para rodar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
