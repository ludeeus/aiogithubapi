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

test: ## Run all tests
	@poetry run pytest tests -rxf -x -vv -l -s --cov=./ --cov-report=xml

build: ## Build the package
	@poetry build

lint: isort black ## Lint all files

coverage: ## Check the coverage of the package
	@poetry run pytest tests -rxf -x -v -l --cov=./ --cov-report=xml > /dev/null
	@poetry run coverage report

isort:
	@poetry run isort aiogithubapi tests

isort-check:
	@poetry run isort aiogithubapi tests --check-only

black:
	@poetry run black --fast aiogithubapi tests

black-check:
	@poetry run black --check --fast aiogithubapi tests
