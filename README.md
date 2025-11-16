QRKot - сервис для сбора пожертвований на пблаготворительные проекты.

Используемые технологии:
Python 3.10, FastAPI, SQLAlchemy, Alembic, PostgreSQL/SQLite, Pytest

Руководство по локальному запуску:

Клонирование репозитория:
git clone https://github.com/SergeyGusev1/cat_charity_fund.git
cd cat_charity_fund

Создать и активировать виртуальное окружение:
python -m venv venv
source venv/Scripts/activate

Установить зависимости:
pip install -r requirements.txt

Создать файл .env:
cp .env.example .env

Заполнить файл .env. Пример:
APP_TITLE=Сервис пожертвований
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=secret

Запустить миграции:
alembic upgrade head

Запустить проект:
uvicorn app.main:app --reload


OpenAPI по адресу:
http://127.0.0.1:8000/docs
