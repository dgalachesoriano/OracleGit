# Ruta principal de la app (ajusta si cambias el layout)
APP_DIR=core/application

.PHONY: test coverage html open-html lint format all

# Ejecuta tests con cobertura en consola
test:
	pytest --cov=$(APP_DIR) --cov-report=term-missing

# Crea un informe HTML de cobertura
coverage:
	pytest --cov=$(APP_DIR) --cov-report=html

# Abre el informe HTML (solo en macOS)
open-html:
	open htmlcov/index.html

# Linting del código con flake8
lint:
	flake8 $(APP_DIR) tests

# Formateo automático con black
format:
	black $(APP_DIR) tests

# Ejecuta todo
all: format lint test coverage open-html
