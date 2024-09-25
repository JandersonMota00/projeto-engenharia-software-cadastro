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

RUN mkdir /data
ENV SQLITE_PATH=/data/db.sqlite3
RUN mkdir /data/staticfiles
ENV STATICFILES_PATH=/data/staticfiles

RUN python manage.py collectstatic --noinput
RUN python manage.py spectacular --color --file schema.yml
RUN python manage.py devseed

# Exponha a porta que o Django usará
EXPOSE 8000

# Comando para iniciar o servidor Gunicorn
CMD ["/app/entrypoint.sh"]
# CMD ["gunicorn", "fraternodjango.wsgi:application", "--bind", "0.0.0.0:8000"]
