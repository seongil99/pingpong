all:
	docker compose up -d --build

dev:
	docker compose -f docker-compose.develop.yml down
	docker compose -f docker-compose.develop.yml up -d --build

# 로그 확인
debug:
	docker compose -f docker-compose.develop.yml down
	docker compose -f docker-compose.develop.yml up --build --force-recreate

re:
	docker compose down
	docker compose up -d --build

clean:
	docker compose down

fclean:
	docker compose down -v

fcleandev:
	docker compose -f docker-compose.develop.yml down -v

.PHONY: all debug re clean fclean
