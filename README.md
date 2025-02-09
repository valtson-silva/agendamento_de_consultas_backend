# Sistema backend para o agendamento de consultas médicas

## 📖  Descrição

Este projeto é um sistema web desenvolvido em Django para facilitar a marcação e gerenciamento de consultas médicas. 
O sistema permite que pacientes agendem consultas com profissionais de saúde, e 
recebam notificações automáticas sobre compromissos futuros.

<br/>

## 🛠️ Funcionalidades

- Cadastro e Login (Pacientes e Profissionais de Saúde)
- Agendamento de Consultas
- Notificações Automáticas via e-mail
- Histórico de Consultas
- Gestão de Profissionais e Especialidades Médicas
- Integração com Banco de Dados
- Docker para Implantação
<br/>

## 📡 Tecnologias utilizadas 
<div align="center"> 
<img align="left" alt="Python" height="30" width="30" src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg">
<img align="left" alt="Django" height="30" width="45" src="https://static.djangoproject.com/img/logos/django-logo-negative.svg">
<img align="left" alt="Postgresql" height="30" width="30" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original.svg">
<img align="left" alt="docker" height="32" width="35" src="https://github.com/user-attachments/assets/6198150a-b145-449c-ad48-cc12f138bd95">
<img align="left" alt="redis" height="38" width="47" src="https://github.com/user-attachments/assets/0f604e51-e697-4358-b3b5-7f002b52ec58">
<img align="left" alt="celery" height="32" width="35" src="https://docs.celeryq.dev/en/stable/_static/celery_512.png">
</div>
<br/><br/>

## ⏳ Inicialização

Esse projeto foi desenvolvido em ambiente Linux, utilizando as tecnologias citadas anteriormente. Sugiro que você prepare o seu ambiente seguindo os passos abaixo:

A preparação do ambiente consiste em instalar as tecnologias citadas anteriormente de acordo com seu sistema operacional.

Para instalar o Python, acesse: https://www.python.org/downloads/

Para instalar o Postgresql, acesse: https://www.postgresql.org/download/

Para instalar o Docker, acesse: https://www.docker.com/

Execute esses comandos no terminal para usar o docker e rodar o projeto:
```
# 1. Construir a imagem do Docker
docker-compose build

# 2. Subir os containers
docker-compose up -d
```
Execute esse comando no terminal para executar os testes:
```
docker-compose run --rm web pytest
```

<br/>

## 🔮 Implementações futuras
1. Implementar pagamentos online

2. Implementar prontuário eletrônico completo

3. Implementar sistema de avaliação de profissionais

<br/>

## 🔎 Status do Projeto

![Badge em Desenvolvimento](https://img.shields.io/badge/Status-Em%20Desenvolvimento-green)
