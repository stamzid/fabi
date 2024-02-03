# Base Image
FROM python:3.11-slim as base
ENV PYTHONUNBUFFERED=true
WORKDIR /fabi

# Builder Stage
FROM base as builder
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY ./pyproject.toml ./pyproject.toml
RUN poetry install --no-interaction --no-ansi -vvv

# Runtime Stage
FROM base as runtime
COPY --from=builder /fabi/.venv /fabi/.venv
ENV PATH="/fabi/.venv/bin:$PATH"
ENV GRPC_DNS_RESOLVER=native
COPY ./ /fabi
CMD python -m fabi.app
EXPOSE 8000

ENTRYPOINT uvicorn fabi.app:server --host 0.0.0.0 --port 8000
