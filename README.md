# Discord Transform for Maltego

## Описание

Transform для Maltego, который получает информацию о пользователе Discord по его ID. Возвращает имя пользователя, дискриминатор, ID, ссылку на профиль и аватар.

---

## Требования

- Python 3.7 или выше
- Maltego Desktop (Community или Commercial)
- Discord аккаунт
- Интернет-соединение

---

## УСТАНОВКА

### Шаг 1: Скачивание трансформа

**Способ A: Через Git**

```bash
git clone https://github.com/ВАШ_НИК/discord-maltego-transform.git
cd discord-maltego-transform
```

**Способ B: Через ZIP**

1. Перейдите на страницу репозитория
2. Нажмите на кнопку "Code"
3. Выберите "Download ZIP"
4. Распакуйте архив в удобную папку (например, C:\Maltego\Transforms\discord)


## Получение Discord токена

Способ A: Через браузер (рекомендуется)

    Откройте Discord в браузере: https://discord.com/app

    Войдите в свой аккаунт

    Нажмите клавишу F12 для открытия Developer Tools

    Перейдите на вкладку Network (Сеть)

    В поле фильтра введите: /api/v9/users/@me

    Обновите страницу (клавиша F5)

    В списке запросов кликните на тот, который появился

    В правой панели найдите раздел Request Headers

    Найдите строку authorization: mfa.xxxxx или authorization: NDcx...

    Скопируйте ВСЁ значение после authorization: 

Как выглядит токен:
NDcxMjM0NTY3ODkwMTIzNDU2.GXvQ7R.abcdefghijklmnopqrstuvwxyz123456

Способ B: Через приложение Discord (альтернативный)

    Закройте Discord полностью (через системный трей)

    Нажмите Win + R, введите %appdata%/discord/Local Storage/leveldb/

    Нажмите Enter

    Найдите файлы с расширением .log

    Откройте их блокнотом (самые большие файлы)

    Найдите строку, содержащую "token"

    Скопируйте значение токена

# Проверка работы 

```bash
cd C:\путь\к\папке\с\трансформом
python discord_transform.py 123456789012345678
```

## Импорт в Maltego

Шаг 1: Открыть Maltego

Запустите Maltego Desktop на вашем компьютере.
Шаг 2: Открыть управление трансформами

В верхнем меню выберите:
Manage → Transforms
Или нажмите сочетание клавиш Ctrl + T

Шаг 3: Импорт нового трансформа
Нажмите кнопку "Import Transform" → выберите "Local"

Шаг 4: Заполнение параметров трансформа

Откроется окно добавления трансформа. Заполните следующие поля:

Поле	            Значение
Display Name	    Discord User Info
Description	Get   information about Discord user by ID
Transform Type	  Local
Command	python
Parameters	      "C:\путь\к\папке\discord_transform.py" %value%
Working Directory	 C:\путь\к\папке\
Timeout (ms)	     30000

Важно:

    Путь к скрипту должен быть ПОЛНЫМ

    Обязательно используйте %value% с процентами

    Если путь содержит пробелы, заключите его в кавычки

Пример для Windows:

    Command: python

    Parameters: "C:\Maltego\Transforms\discord\discord_transform.py" %value%

    Working Directory: C:\Maltego\Transforms\discord

Пример для Linux/Mac:

    Command: python3

    Parameters: "/home/user/maltego/transforms/discord_transform.py" %value%

    Working Directory: /home/user/maltego/transforms

Шаг 5: Назначение на сущность

    Нажмите кнопку "Next"

    В открывшемся окне выберите вкладку "Entities"

    Найдите и выберите сущность: maltego.Identifier

    Нажмите "Add"

    Убедитесь, что сущность появилась в списке справа

Опционально: Вы также можете назначить трансформ на сущности:

    maltego.Person

    maltego.Phrase

Шаг 6: Завершение

    Нажмите "Next"

    Проверьте настройки

    Нажмите "Finish"

