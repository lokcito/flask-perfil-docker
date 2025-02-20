build:
	docker build . -t ghcr.io/lokcito/flask-perfil-docker:latest

push:
	docker push ghcr.io/lokcito/flask-perfil-docker:latest
