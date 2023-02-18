prod: down
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

dev: down
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

down:
	docker compose down --remove-orphans --rmi all --volumes --timeout 0
