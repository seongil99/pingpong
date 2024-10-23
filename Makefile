all:
	docker compose up -d

dev:
	docker compose up --build

re:
	docker compose down
	docker compose up -d

clean:
	docker compose down

.PHONY: all debug re clean