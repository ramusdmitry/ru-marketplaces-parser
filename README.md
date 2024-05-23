# RU Marketplaces Parser [YANDEX + WB]

## Описание

## Запуск

### Создание виртуального окружения и установка зависимостей
```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


### Запуск MySQL в Docker
```shell
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=prices_db -p 3306:3306 -d mysql:8.0
```

### Инициализация Alembic
```shell
alembic init alembic
```


### Измените alembic.ini, чтобы указать строку подключения
```shell
sqlalchemy.url = mysql+mysqlconnector://root:my-secret-pw@localhost/prices_db
```

### Настройка alembic/env.py
```shell
from your_project.models import Base
target_metadata = Base.metadata
```

### Создание первой миграции
```shell
alembic revision --autogenerate -m "Initial migration"
```

### Применение миграции
```shell
alembic upgrade head
```

### Создайте и пропишите в файле `.env` токен вашего бота
```shell
TELEGRAM_BOT_TOKEN = "your-bot-token"
```

### Запуск бота
```shell
pyton run.py
```
