# Author: Marc Nebel
# Beschreibung: Dockerfile für Data Analyzer Container

FROM python:latest

RUN mkdir /root/src
WORKDIR /root/src

COPY . .

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive TZ="Germany/Berlin" apt-get install -y curl gnupg nano python3 python3-pip libpq-dev tzdata
    
RUN pip install --no-cache-dir -r requirements.txt


RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
