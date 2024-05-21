# О сервисе

## Настройка

```shell
python3 -m venv .venv/
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

### Запускаем MySQL в docker

```shell
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=prices_db -p 3306:3306 -d mysql:8.3
```

### Применяем миграции

```shell
alembic init alembic
```

Затем меняем в файле alembic.ini
```text
[alembic]
sqlalchemy.url = mysql+mysqlconnector://root:my-secret-pw@localhost/prices_db
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
