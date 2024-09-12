# Usar uma imagem base do Python
FROM python:3.12

# Instalar Nginx e outras dependências
RUN apt-get update && apt-get install -y \
    nginx \
    sqlite3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar o código-fonte e arquivos de configuração
COPY atendimentoFraternoBackend /app/atendimentoFraternoBackend/
COPY frontend /var/www/html/
COPY nginx.conf /etc/nginx/nginx.conf

# Instalar dependências do Python
RUN pip install --no-cache-dir -r /app/atendimentoFraternoBackend/requirements.txt

# Expor as portas para o Nginx e o Django
EXPOSE 80 8000

# Copiar o script de inicialização e garantir permissões
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Comando para iniciar Nginx e Django
CMD ["/start.sh"]
