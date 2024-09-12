# Use a imagem base oficial do Python 3.12
FROM python:3.12.0-slim

# Instale dependências do sistema
RUN apt-get update \
    && apt-get install -y \
       build-essential \
       libsqlite3-dev \
       gcc \
       graphviz-dev \
    && rm -rf /var/lib/apt/lists/*

# Crie e defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos e instale as dependências do Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação para o contêiner
COPY . /app/

# Execute as migrações do Django
RUN python manage.py migrate
RUN python manage.py devseed

RUN python manage.py collectstatic --noinput

# Exponha a porta que o Django usará
EXPOSE 8000

# Comando para iniciar o servidor Gunicorn
CMD ["gunicorn", "fraternodjango.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["bash", "fraterno_init.sh"]
