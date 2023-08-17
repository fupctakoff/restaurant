# restaurant
# О проекте
<br>
Стек: FastAPI,  PostgreSQL, SQLAlchemy, Redis, Pydantic, Pytest, Docker

# Установка
<br>

### 1) Клонировать репозиторий с проектом

    git clone https://github.com/fupctakoff/restaurant.git

### 2) Изменить настройки подключения к базе данных, поменяв значения переменных в файле .env в корне проекта. .env.example доступен также в корне проекта

# Запуск

### 1) Запуск проекта без тестов
  
  docker compose up

### 1.1) Запуск тестов -> вывод в консоли

    docker compose -f docker-compose-tests.yml up

#### Примечание

Проект доступен на порту 8000. Исполняемый файл находится: src/main.py

<br>
