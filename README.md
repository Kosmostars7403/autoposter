# Скрипт постинга в VK, Telegram, Facebook по расписанию

Скрипт для постинга в социальные сети по расписанию в Google Spreadsheets.

### Как установить

Для запуска программы у вас уже должен быть установлен Python 3. 

Установите зависимости командой в терминале:

```
$ pip install -r requirements.txt
```

Чтобы начать постинг, в каждой соц сети придется получить токен.
1. для телеграмм [инструкция](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/)
2. для VK [инструкция](https://devman.org/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/)
3. для Facebook [инструкция](https://developers.facebook.com/docs/graph-api/explorer/)
4. для Google Spreadsheets пройдите первый пункт туториала [инструкция](https://developers.google.com/sheets/api/quickstart/python)
5. для  Google Drive создайте приложение [инструкция](https://gsuitedevs.github.io/PyDrive/docs/build/html/quickstart.html#authentication)
6. в той же консоле, где создаете приложение для Drive создайте ключ API для созданного ранее приложения таблиц

После всех мучений с получением токенов создайте файл .env и заполните следующим образом:

`CLIENT_ID`=выдается при регистрации приложения таблиц

`CLIENT_SECRET`=выдается при регистрации приложения таблиц

`SPREADSHEET_ID`=id_таблицы

`GOOGLE_SHEETS_API_KEY`=API_ключ_таблицы

`VK_USER_TOKEN`=ваш_токен_ВК

`VK_USER_LOGIN`=ваш_логин_ВК

`VK_GROUP_ID`=id_вашей_группы_ВК(цифры из ссылки на группу)

`VK_ALBUM_ID`=id_альбома_вашей_группы_ВК(цифры из ссылки на альбом группы вк)

`TELEGRAM_TOKEN`=токен_телеграм_бота

`TELEGRAM_CHANNEL_ID`=ссылка_на_канал(например: @my_channel_is_awesome)

`FACEBOOK_TOKEN`=токен_фейсбук

`FACEBOOK_GROUP_ID`=id_группы_фейсбук(цифры из ссылки на группу)

[Пример заполнения таблицы](https://docs.google.com/spreadsheets/d/17r4QRW_m0clut772bRnUL-U1-JiazImiZMm43SkgS9Q/edit#gid=0)

### Пример запуска скрипта 
```
$python3 autoposter.py
```
С этого момента скрипт начинает раз в 60 секунд проверять таблицу и выкладывать посты в соответствии с расписанием.


### Пример запуска скрипта vk_tg_fb_posting.py в ручном режиме
Скрипт принимает на вход два обязательных аргумента, путь до изображения и путь до текстового файла с самим постом(*.txt)
```
$python3 vk_tg_fb_posting.py image.jpg text.txt
```

Используя дополнительные аргументы, вы можете пропустить постинг в определенную соцсеть.
1. `-pf` или `--post_facebook` - выложить в Facebook
2. `-pv` или `--post_vk` - выложить во Вконтакте
3. `-pt` или `--post_telegram` - выложить в Телеграм

Пример:
```
$python3 vk_tg_fb_posting.py image.jpg text.txt -pt
```
Такой ввод запустит скрипт на постинг только в телеграм!

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
