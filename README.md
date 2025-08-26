# BaseBot TEMPLATE

![Basebot](./img/baner.jpg)

> [!IMPORTANT]
> Должен быть установлен Python3.11 и python3.11-venv для разработки

> [Установка Python3.11](https://zomro.com/rus/blog/faq/473-installing-python-311-on-ubuntu-2204)

> [!NOTE]
> Может понадобиться Docker

> [Установка Docker](https://timeweb.com/ru/community/articles/kak-ustanovit-docker-na-ubuntu-22-04)

## Конфигурация
- Эта версия проекта работает с PostgreSQL
- Доступен скрипт Docker
- Создайте `.env` как `.BaseBot.env.example`, предварительно создав токен бота в Botfather.

## Как запустить локально
1. Установите всё, что нужно командой `make install`
2. Запустите `make`
3. Деинсталировать `make uninstall`

## Как развернуть на сервере linux
- Запускаем сборку проекта
```bash
docker compose  up -d --build basebot_app
```
- Запустить контейнеры
```bash
docker-compose up
```

- Эта команда позволяет останавливать и удалять контейнеры и другие ресурсы, созданные командой docker-compose up:
```bash
$ docker-compose down
```

- Эта команда выводит журналы сервисов:
```bash
$ docker-compose logs -f [service name]
```
Например, в нашем проекте её можно использовать в таком виде: $ docker-compose logs -f [service name].

- С помощью такой команды можно вывести список контейнеров:
```bash
$ docker-compose ps
```
- Данная команда позволяет выполнить команду в выполняющемся контейнере:
```bash
$ docker-compose exec [service name] [command]
```
Например, она может выглядеть так: docker-compose exec server ls.

- Такая команда позволяет вывести список образов:
```bash
$ docker-compose images
```
- Остановить проект
```bash
docker compose stop basebot_app
```
- 
# basebot_template
