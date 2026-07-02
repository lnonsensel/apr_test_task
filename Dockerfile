FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

RUN apt-get update && apt-get install -y gcc libpq-dev python3-dev && apt-get upgrade -y && apt-get clean

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY requirements.txt ./

RUN uv pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY main.py config.py ./

EXPOSE 3000

CMD ["python", "main.py"]
