.DEFAULT_GOAL := help

help: ## Shows this help message
	@printf "\033[1m%s\033[36m %s\033[32m %s\033[0m \n\n" "Development environment for" "ludeeus/aiogithubapi" "";
	@awk 'BEGIN {FS = ":.*##";} /^[a-zA-Z_-]+:.*?##/ { printf " \033[36m make %-25s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST);
	@echo

requirements: install-poetry ## Install requirements
	@poetry install
	@poetry check

install: ## Install aiogithubapi
	@poetry install

install-poetry:
	@curl -sSL https://install.python-poetry.org | python3 -

build: ## Build the package
	@poetry build

test: ## Run all tests
	@poetry run pytest tests -rxf -x -v -l --cov=./ --cov-report=xml

lint: isort black ## Lint all files

generate: ## Generate models
	@poetry run datamodel-codegen --url https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json --output aiogithubapi/generated_models.py --input-file-type openapi --reuse-model --use-default --target-python-version 3.8 --use-schema-description --use-standard-collections --strict-nullable --snake-case-field --use-annotated

coverage: ## Check the coverage of the package
	@poetry run pytest tests -rxf -x -v -l --cov=./ --cov-report=xml > /dev/null
	@poetry run coverage report --skip-covered

isort:
	@poetry run isort aiogithubapi

isort-check:
	@poetry run isort aiogithubapi --check-only

black:
	@poetry run black --fast aiogithubapi

black-check:
	@poetry run black --check --fast aiogithubapi
