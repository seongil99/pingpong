FROM python:3.13.0-bookworm

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x /app/docker-entrypoint.sh

RUN mkdir -p /app/media

EXPOSE 8000

CMD [ "./docker-entrypoint.sh" ]
