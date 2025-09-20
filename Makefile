lint:
	uvx ruff check
	uvx ruff check --fix-only .

lint_test:
	echo "Lint tests"

format:
	uvx ruff format .