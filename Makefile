all:
	docker compose up -d

re:
	docker compose down
	docker compose up -d

clean:
	docker compose down
