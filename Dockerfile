FROM python:3.12-slim-bookworm

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y sqlite3 libsqlite3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /ROOT

# install packages
COPY Makefile pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy database 
COPY sql ./sql
COPY bin ./bin

# copy module 
COPY backend ./backend

# install module 
RUN pip install --no-cache-dir -e .

# set executable permission and create db
RUN chmod +x ./bin/backenddb
RUN ./bin/backenddb create

ENTRYPOINT [ "flask", "--app", "backend", "run", "--host", "0.0.0.0", "--port", "5000"]