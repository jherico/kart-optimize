FROM node:18-buster
LABEL maintainer="Leo Davis <leo@saintandreas.org>"

RUN apt-get update && apt-get install -y python3-pip
