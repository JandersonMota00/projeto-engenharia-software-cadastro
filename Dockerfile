# Usar uma imagem base do Ubuntu
FROM ubuntu:22.04

# Instalar dependências básicas
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    curl \
    wget \
    vim \
    git \
    nginx \
    sqlite3 \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update

# Instalar Python 3.12
RUN apt-get install -y python3.12 python3.12-venv python3.12-dev

# Definir o Python 3.12 como padrão
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Instalar pip e as dependências do projeto
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar o código da aplicação
COPY . /app
WORKDIR /app

# Configurar Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Expor portas para Nginx e Django
EXPOSE 80 8000

# Comando para iniciar Nginx e Django
CMD service nginx start && python3.12 manage.py runserver 0.0.0.0:8000
