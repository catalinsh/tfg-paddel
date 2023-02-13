FROM python:3.10-slim AS base

WORKDIR /api

COPY ./app/api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/api/src ./src
COPY ./paddel /paddel


FROM base AS production

RUN pip install --no-cache-dir /paddel

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--root-path", "/api"]


FROM base AS development

RUN pip install --no-cache-dir -e /paddel

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--root-path", \
     "/api", "--reload", "--reload-dir", ".", "--reload-dir", "/paddel"]