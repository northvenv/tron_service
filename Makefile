DC = docker-compose
LOGS = docker logs
EXEC = docker exec -it

COMPOSE_FILE = docker-compose.yaml
APP_CONTAINER = tron_service

.PHONY: app
app:
	${DC} -f ${COMPOSE_FILE} up --build 

.PHONY: app-down
app-down:
	${DC} -f ${COMPOSE_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} poetry run alembic upgrade head

.PHONY: makemigrations
makemigrations:
	${EXEC} ${APP_CONTAINER} poetry run alembic revision --autogenerate -m "$(m)"