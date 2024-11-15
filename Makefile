all:
	docker compose up -d --build

dev:
	docker compose -f docker-compose.develop.yml down
	docker compose -f docker-compose.develop.yml up -d --build

re:
	docker compose down
	docker compose up -d --build

clean:
	docker compose down

fclean:
	docker compose down -v

.PHONY: all debug re clean fclean
