docker-up: docker-down
	docker-compose up -d -t 0

docker-up-dev: docker-down
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d -t 0

docker-restart:
	docker-compose restart -t 0

docker-down:
	docker-compose down -v -t 0

docker-clean:
	docker-compose down --rmi all -v -t 0