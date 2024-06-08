SHELL := /bin/bash

debug:
	flask --app backend  --debug run --host 0.0.0.0 --port 5000

run:
	flask --app backend  run --host 0.0.0.0 --port 5000

docker-run:
	docker run --gpus all --env-file .env -it -p 5000:5000 -d backend

docker-build:
	docker build -t backend .

