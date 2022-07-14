SHELL:=/bin/bash
VERSION=3.0

up:
	firefox localhost &
	set -o allexport;\
	source redis/redis.env;\
	source azure.env;\
	set +o allexport;\
	docker-compose up --build

build:
ifdef nocache
	docker build --no-cache -t qfortier/mtgscan-server:$(VERSION) server/
else
	docker build -t qfortier/mtgscan-server:$(VERSION) server/
endif

push: build
	docker push qfortier/mtgscan-server:$(VERSION)
