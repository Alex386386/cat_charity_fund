# ЯП - Спринт 22 - Проект сбора пожертвований на нужды котиков написанный на FastAPI.

### Описание

Проект реализующий возможность регистрации пользователя, и отправки им донатов на реализацию благотворительных проектов на благосостояние котиков.

## Stack

Python 3.8, FastAPI 0.78

### Установка, Как запустить проект:
https://github.com/Alex386386/cat_charity_fund
Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить проект:

```
uvicorn app.main:app --reload
```

Документация по API проекта можно найти в файле openapi.json, запустить её можно на сайте redoc.

Автор:
- [Александр Мамонов](https://github.com/Alex386386) 
