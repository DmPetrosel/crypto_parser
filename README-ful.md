[Устанавливаем postgresql](https://www.postgresql.org/download/macosx/)

[Устанавливаем python3.11](https://www.python.org/downloads/macos/)

[Устанавливаем Android Studio](https://developer.android.com/studio?hl=ru)

Заходим в @botfather и создаём бота, получаем токен и вставляем в .env

Командная строка
```bash
sudo su - postgres
psql
CREATE USER crypto_parser with password '1234';
CREATE DATABASE crypto_parser_db with owner crypto_parser;
\q
exit
```
Устанавливаем все
```bash
make install
```
Переходим в Android Studio,скачиваем эмулятор Pixel 9 API 35, создаём проекти запускаем эмулятор

Пишем `adb devices` в терминале, должно быть что-то вроде emulator-5554
В файле `module.py` меняем `device = Device("emulator-5554")` на `device = Device("emulator-5554")`

запускаем
```bash
make
```
останвливаем
и запускаем снова

Работает!
![Basebot](./img/baner.jpg)