FROM python:3.9-slim AS base
WORKDIR /code

COPY ./app/api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./paddel ./paddel
RUN pip install --no-cache-dir --upgrade -e ./paddel

COPY ./app/api/app ./app


FROM base AS production
CMD [ \
    "sh", "-c", \
    "uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 80 \
    --root-path ${PUBLIC_API_PATH}" \
    ]


FROM base AS development
CMD [ \
    "sh", "-c", \
    "uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 80 \
    --root-path ${PUBLIC_API_PATH} \
    --reload \
    --reload-dir ./app \
    --reload-dir ./paddel" \
    ]
