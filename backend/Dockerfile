FROM python:3.13.0-bookworm

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apt update && apt install -y dumb-init && rm -rf /var/lib/apt/lists/*

COPY . .
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

CMD [ "/usr/bin/dumb-init", "--", "/app/docker-entrypoint.sh" ]