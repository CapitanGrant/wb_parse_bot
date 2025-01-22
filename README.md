# Cистема получения и хранения информации с wb

Приложение на основе FastAPI для сбора данных о товарах с Wildberries, предоставляющее доступ к информации о товарах через Telegram-бота (aiogram). Функциональность включает извлечение информации о товарах (название, артикул, цена, рейтинг и т.д.), хранение данных в базе данных (SQLAlchemy), управление миграциями (Alembic), удобное логирование (Loguru) и Telegram-интерфейс для пользователей.
## Стек технологий

- **Веб-фреймворк**: FastAPI
- **ORM**: SQLAlchemy
- **База данных**: PostgeSQL
- **Система миграций**: Alembic

## Зависимости проекта

- `fastapi[all]==0.115.0` - высокопроизводительный веб-фреймворк
- `aiogram==3.15.0` - асинхронный фреймворк для создания Telegram-ботов
- `loguru==0.7.2` - красивое и удобное логирование
- `pydantic-settings==2.7.0` - управление настройками приложения
- `SQLAlchemy==2.0.35` - ORM для работы с базами данных
- `pydantic==2.9.2` - валидация данных
- `alembic==1.14.0` - управление миграциями базы данных
- `fastapi[all]==0.115.0` - высокопроизводительный веб-фреймворк
- `python-dotenv~=1.0.1` - загрузка переменных окружения из .env файла
- `apscheduler==3.11.0` - библиотека для планирования задач
- `requests==2.32.3` - библиотека для выполнения HTTP-запросов
- `urllib3==2.3.0` - HTTP-клиент с поддержкой пула соединений



## Запуск приложения

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/CapitanGrant/wb_parse_bot
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Создайте и настройте `.env` файл:

   ```env
   DB_USER=postgres_user
   DB_PASSWORD=postgres_password
   DB_HOST=localhost
   DB_PORT=5433
   DB_NAME=postgres_db
   API_TOKEN=ваш тг токен
   TG_HOST=0.0.0.0
   TG_PORT=80
   BASE_URL=ваш url ngrok

   
   ```
4. Запустите docker контейнер c PostgreSQL:

   ```bash
   docker compose up -d
   ```



## Миграции базы данных

1. Инициализируйте Alembic:

   ```bash
   cd app
   alembic init -t async migration
   ```

   Затем переместите `alembic.ini` в корень проекта.

2. В `alembic.ini` установите `script_location` как `app/migration`.
3. В migrations/env.py замените импорты и код до target_metadata на
```env
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))

import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.config import database_url
from app.dao.database import Base
from app.products.models import Product

config = context.config
config.set_main_option("sqlalchemy.url", database_url)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```
4. Создайте миграцию:

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

5. Примените миграции:

   ```bash
   alembic upgrade head
   ```
6. Для запустите приложение FastAPI app/main.py:
    ```bash
   uvicorn app.main:app --reload
   ```
7. Для запустите файл /main.py:
    ```bash
   cd bot
   run main.py
   ```
