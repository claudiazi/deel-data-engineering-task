export DESKTOP_PATH := $(HOME)/Desktop

ifndef DOCKER_PLATFORM
	export DOCKER_PLATFORM=linux/amd64
endif

check-%:
	@if [ "${${*}}" = "" ]; then \
		echo -e "${RED} Variable $* not set ❌${RESET}"; \
		exit 1; \
	fi

clean: ##-local- Cleanup project
	rm -rf venv
	rm -rf venvs
	rm -rf logs
	rm -rf var

install-dev: ##-local- Setup project for dev
install-dev: clean
	set -e; \
	virtualenv -p python3.11 venv; \
	pip install --ignore-installed -r dev-requirements.txt -r requirements.txt; \
	pre-commit install


run-ingestion-local:
	@echo "Running ingestion-sync..."
	python ingestion/airbyte_sync.py

run-transformation-local:
	cd ${PWD}/transformation && \
	bash run_dbt.sh

run-report-automation-local:
	cd ${PWD}/report_automation && \
	python csv_report.py

docker-build: ##-local- Build Docker image | args: service
docker-build: check-service
	docker build \
	--platform ${DOCKER_PLATFORM} \
	-t ${service}:latest ./${service}

docker-run: ##-local- Run Docker image | args: service, cmd
docker-run: check-service docker-build
	@echo "Running docker image for ${service}"
	@docker run -it --rm \
	--platform ${DOCKER_PLATFORM} \
	${service}:latest ${cmd}


docker-compose-up: ##-local- Start docker compose
	@echo "Starting docker compose..."
	docker-compose up
	@echo "Docker compose started."

