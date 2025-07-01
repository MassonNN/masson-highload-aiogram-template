![template](https://github.com/user-attachments/assets/ca269ab5-095b-415e-893b-53e6a5d23632)
![](https://img.shields.io/badge/version-0.1.0%20-brightgreen)
![](https://img.shields.io/github/license/MassonNN/masson-highload-aiogram-template)
![](https://img.shields.io/github/forks/MassonNn/masson-highload-aiogram-template)
![](https://img.shields.io/github/stars/MassonNn/masson-highload-aiogram-template?style=flat-square)
[![telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/massonnn_yt)

---
## Setup bot

1. Clone this repository

2. Change the name of `.env.dist` to `.env` and set all environment variables as you need

3. Change password for redis in build/redis.conf (`requirepass` and `masterauth`). Set same password in `.env` 
   (`REDIS_PASSWORD`).

4. Change project name and other information in `pyproject.toml`

---
## Development

If you want to lint your code: \
```make lint``` \
This will start isort, blue and ruff to src and tests folders

You can manually run any instrument by: \
`make ruff`, `make blue` or `make isort`

### Migrations
`make generate NAME=<name>` \
Generate alembic revision for migration with given name

`make migrate` \
Apply migrations to the target database

---
## Deployment
First of all, I very recommend you to deploy NATS and PostgreSQL directly on your server without Docker. So, in any 
way you have to configure both to your needs because I cant create configurations for without any understanding of 
your app goals and requirements.

1) Your app exists as one united Docker image which you have to create with \
`docker build --file ./buildfiles/Dockerfile --tag <YOUR_APP_NAME> .`


2) Replace YOUR_APP_NAME to something like `my_app:latest` and set this to image in app services in docker-compose.yml 
(bot, scheduler, worker, migrations)


3) Every time you start docker-compose you have to rebuild app image or you can do it automatically by changing 
   image section to:
```yml
build:
   context: .
   dockerfile: buildfiles/Dockerfile
```
But this doesn't work when you deploy app to a server.

4) To deploy your app on a server you have to upload app image to Docker Registry (such as official hub.docker.com 
   or any other, I suggest deploy your own custom Docker Registry since it doesn't require too many 
   resources and make your life much better)

