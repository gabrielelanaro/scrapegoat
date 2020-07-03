format:
	black .
	isort -rc --atomic .

test:
	PYTHONPATH=. pytest -v

build:
	docker-compose build

run-server:
	python -m scrapegoat.app immoscout/store/fe5c6fdcc9812424df4edcef72a49a50ce7a9553d9b2c4d887e881cc986d9d10/0003/

develop:
	docker run -v $(CURDIR):/app -p 8081:8081 -it scrapegoat_app:latest /bin/bash

develop-ui:
	docker run -v $(CURDIR)/ui/scrapegoat-ui:/ui -p 8080:8080 -it scrapegoat_ui:latest /bin/bash

.PHONY: format test