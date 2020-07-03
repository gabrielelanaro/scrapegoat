format:
	black .
	isort -rc --atomic .

test:
	PYTHONPATH=. pytest -v

build:
	docker-compose build

create-bridge:
	docker network create scrapegoat_develop

run-server: export DATA_DIR = immoscout/store/fe5c6fdcc9812424df4edcef72a49a50ce7a9553d9b2c4d887e881cc986d9d10/0003/
run-server: 
	adev runserver --port=8081 --host=0.0.0.0 scrapegoat/app.py

run-ui:
	npm run serve

develop:
	docker run --rm -v $(CURDIR):/app -p 8081:8081 --name app --network scrapegoat_develop -it scrapegoat_app:latest /bin/bash

develop-ui:
	docker run --rm --network="scrapegoat_develop" -v $(CURDIR)/ui/scrapegoat-ui:/ui --name ui -p 8080:8080 -it scrapegoat_ui:latest /bin/bash

.PHONY: format test