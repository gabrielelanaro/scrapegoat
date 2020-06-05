format:
	black .
	isort -rc --atomic .

test:
	PYTHONPATH=. pytest -v


.PHONY: format test