# specify the node base image with your desired version node:<version>
FROM node:10
# replace this with your application's default port
EXPOSE 8888

WORKDIR /ui

COPY package.json .
COPY tsconfig.json .
COPY public public
COPY src src
COPY vue.config.js .


RUN npm i
