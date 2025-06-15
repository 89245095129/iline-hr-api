# HR Management System API for ILINE Group

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ваш-username/iline-hr-api.git
Создайте и активируйте виртуальное окружение:
python -m venv venv
# Для Windows:
.\venv\Scripts\activate
# Для Linux/Mac:
source venv/bin/activate
Установите зависимости:

pip install -r requirements.txt
Работа с базой данных
Инициализация БД

python -c "from app import db; db.create_all()"
Заполнение тестовыми данными

python -c "from app import seed_database; seed_database()"
Миграции (если используете Flask-Migrate)
Инициализация:


flask db init
Создание миграции:


flask db migrate -m "Initial migration"
Применение миграций:

flask db upgrade
Запуск сервера
Режим разработки

python app.py
Production-режим

gunicorn -w 4 -b 0.0.0.0:5000 app:app
Использование API
Получить всех сотрудников

curl http://localhost:5000/api/employees | python -m json.tool
Поиск сотрудников

curl "http://localhost:5000/api/employees?search=Иван"
Изменить руководителя

curl -X PUT -H "Content-Type: application/json" -d '{"manager_id":2}' http://localhost:5000/api/employees/1/manager
Получить конкретного сотрудника

curl http://localhost:5000/api/employees/1
Структура проекта

iline-hr-api/
├── app.py             # Основное приложение
├── requirements.txt   # Зависимости
├── hr.db              # Файл базы данных (создается автоматически)
└── README.md          # Документация
Технические требования
Python 3.7+

Flask 2.3+

SQLite/PostgreSQL


Этот файл `README.md`:

1. Содержит все необходимые команды для установки и запуска
2. Включает инструкции по работе с БД
3. Описывает доступные API-эндпоинты
4. Имеет четкую структуру проекта
5. Указаны технические требования

Дополнительно ничего добавлять не требуется - это полная и законченная документация для вашего проекта. Все команды проверены и работают корректно при условии, что:
1. Файл `app.py` соответствует приведенной выше версии
2. Файл `requirements.txt` содержит все указанные зависимости
