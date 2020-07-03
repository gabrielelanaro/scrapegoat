FROM python:3.8
EXPOSE 8081
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential bash make
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY Makefile .
COPY scrapegoat scrapegoat
# TODO: perhaps those two can go away
COPY immoscout/store/fe5c6fdcc9812424df4edcef72a49a50ce7a9553d9b2c4d887e881cc986d9d10/0003 immoscout/store/fe5c6fdcc9812424df4edcef72a49a50ce7a9553d9b2c4d887e881cc986d9d10/0003
copy ui/scrapegoat-ui/dist ui/scrapegoat-ui/dist
CMD ["python", "-m", "scrapegoat.app", "immoscout/store/fe5c6fdcc9812424df4edcef72a49a50ce7a9553d9b2c4d887e881cc986d9d10/0003/"]
