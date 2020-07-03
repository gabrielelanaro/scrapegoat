FROM python:3.7-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers bash make
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY Makefile .
COPY scrapegoat scrapegoat
CMD ["python", "-m", "scrapegoat.app", "immoscout/store/fe5c6fdcc9812424df4edcef72a49a50ce7a9553d9b2c4d887e881cc986d9d10/0003/"]
