all:
	docker compose up -d

dev:
	docker compose up --build --force-recreate

re:
	docker compose down
	docker compose up -d --build

clean:
	docker compose down

.PHONY: all debug re clean
