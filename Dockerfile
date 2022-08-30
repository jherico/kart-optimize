FROM node:18-buster
LABEL maintainer="Leo Davis <leo@saintandreas.org>"

WORKDIR /app

# RUN apt-get update && apt-get install -y python3-pip
COPY src src
COPY public public
COPY package-lock.json .
COPY package.json .

RUN npm install

CMD ["npm", "start"]