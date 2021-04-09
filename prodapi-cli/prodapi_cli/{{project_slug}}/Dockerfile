ARG PYTHON_IMAGE_TAG=3.9.4-slim-buster
FROM python:$PYTHON_IMAGE_TAG

WORKDIR /app

COPY pyproject.toml .

# For supporting CronJobs running inside mTLS-enabled Istio Kubernetes clusters
# See https://github.com/redboxllc/scuttle for info.
COPY --from=redboxoss/scuttle:1.3.4 /scuttle /bin/scuttle

EXPOSE 80/tcp

ENV APP_ENVIRONMENT=development

RUN apt-get update \
    && apt-get install -y curl build-essential \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && poetry install --no-root --no-dev \
    && apt-get purge -y --auto-remove curl build-essential

COPY ./{{ project_slug_underscored }} ./{{ project_slug_underscored }}
RUN poetry install

ARG BUILD_HASH=dev
ENV BUILD_HASH=$BUILD_HASH SENTRY_RELEASE=$BUILD_HASH

CMD ["uvicorn", \
     "{{ project_slug_underscored }}:app", \
     "--log-level=info", \
     "--no-access-log", \
     "--lifespan=on", \
     "--host=0.0.0.0", \
     "--port=80" \
]
