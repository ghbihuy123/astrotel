lint:
	uvx ruff check
	uvx ruff check --fix-only .

lint_test:
	echo "Lint tests"

test:
	echo "Run unittest"

build:
	uv build

format:
	uvx ruff format .