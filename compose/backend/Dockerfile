FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

ENV PYTHONPATH "${PYTHONPATH}:/"

RUN echo "deb http://deb.debian.org/debian testing main" >> /etc/apt/sources.list
RUN apt upgrade && apt update && apt install -y git libpcap-dev nmap  masscan/testing

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./backend/pyproject.toml ./backend/poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY ./backend /app
