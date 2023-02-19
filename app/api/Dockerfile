FROM python:3.9-slim AS base
WORKDIR /code

# Install API dependencies
COPY ./app/api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Install PADDEL dependencies
COPY ./paddel/pyproject.toml ./paddel/pyproject.toml
RUN pip install --no-cache-dir --upgrade ./paddel

COPY ./paddel ./paddel
COPY ./app/api/app ./app


FROM base AS production
RUN pip install --no-deps ./paddel
CMD [ \
    "sh", "-c", \
    "uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 80 \
    --root-path ${PUBLIC_API_PATH}" \
    ]


FROM base AS development
RUN pip install --no-deps -e ./paddel
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
