FROM python:3.9-slim

WORKDIR /api

COPY ./api/requirements.txt ./
COPY ./paddel /paddel

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./api/src ./src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--root-path", "/api"]