# Тестовое задание для "LLC Аналитические программные решения"
Для выполнения задания был использован стек: FastAPI + pydantic + SQLAlchemy\[async\] (asyncpg) + elasticsearch\[async\], Docker/Docker Compose и PostgreSQL 17.

В процессе решения тестового задания ни одна строчка текста не была написана большой лингвистической моделью. От кода, до README были написаны человеком.

# Инструкции по запуску
1) Дописать `.db.env` и `.elastic.env` по шаблонам (`*.example` файлы)
2) `docker compose up --build -d`
3) После запуска всех контейнеров, для заполнения БД и индекса Elasticsearch есть файл `create_sample_data.py`
```
python3 create_sample_data.py
```
Для этого предварительно нужно установить зависимости: asyncio, aiohttp, и pandas
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install asyncio aiohttp pandas
```


# Возможные улучшения
1) Хранить рубрики в отдельной таблице и сохранять связи пост<->рубрика как post_id<->rubric_id
2) Сейчас rubrics для каждого post получаются из БД через
```
rubrics = await db_crud.get_rubrics_ids_for_post(db, post)
return Post.model_validate_with_rubrics(post, rubrics)
```
можно сделать лучше, через единый запрос. Это костыль.
3) Минимальный графический интерфейс
4) Настройки приложения в config.py - можно заменить, так же как и src/elastic/config.py
