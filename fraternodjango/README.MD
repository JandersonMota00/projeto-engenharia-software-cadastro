

Para executar o backend:

Configuração do ambiente no windows (precisa fazer somente uma vez):

Instale o python 3.12 (pode ser baixado na loja de aplicativos do windows)

Abra a pasta fraternodjango no navegador de arquivos

Na parte de cima do navegador de arquivos, ira ter o caminho da pasta,
algo como  .../projeto-engenharia-software-cadastro/fraternodjango,
clique, apague e digite cmd para abrir o terminal nessa pagina

No terminal, digite:

pip install -r requirements.txt

aguarde a instalação terminar

Fim da configuração de ambiente

Como executar:

Existem dois comandos para executar

python manage.py devseed
esse comando ira apagar o banco de dados e recria-lo, não é necessario toda vez más recomendo executalo toda vez que:

For a primeira vez executando
Baixar um novo commit do github
Surgir algum bug inexplicavel


python manage.py runserver
esse comando ira executar o servidor de desenvolvimento do django em localhost:8000