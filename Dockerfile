FROM python:3.12-alpine

WORKDIR /ROOT

COPY sql ./sql
COPY Makefile pyproject.toml requirements.txt ./
COPY backend ./backend

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

ENTRYPOINT [ "flask", "--app", "backend", "run", "--host", "0.0.0.0", "--port", "5000"]