SHELL:=/bin/bash
VERSION=1.0

up: 
	source .env && \
	docker-compose up --build

build:
	docker build -t qfortier/mtgscan-server:$(VERSION) server/

push: build
	docker push qfortier/mtgscan-server:$(VERSION)
