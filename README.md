# О сервисе

## Настройка

```shell
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirmenets.txt
```

## Запуск

### Запускаем MySQL в docker

```shell
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=prices_db -p 3306:3306 -d mysql:latest
```

### Применяем миграции

```shell
alembic init alembic
```

Затем меняем в файле alembic.ini
```text
[alembic]
sqlalchemy.url = mysql+mysqlconnector://prices_user:password@localhost/prices_db
```

Добавляем в alembic/env.py
```python
from storage.models import Base
target_metadata = Base.metadata
```

Применяем миграцию

```shell
alembic upgrade head
```