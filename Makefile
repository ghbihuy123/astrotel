lint:
	uvx ruff check .
	uvx ruff check . --fix

lint_test:
	echo "Lint tests"

test:
	echo "Run unittest"

build:
	uv build

format:
	uvx ruff format .