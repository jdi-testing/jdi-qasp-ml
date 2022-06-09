.PHONY: clean
clean:
	@echo "Cleaning up ..."
	@find . -name \*.pyc -delete
	@find . -name \*.pyo -delete
	@find . -name \__pycache__ -exec rm -rf {} +

.PHONY: lint
lint:
	@echo "Linting ..."
	@flake8 .

.PHONY: unittest
unittest: clean lint
	@echo "Unit tests ..."
	@pytest tests/unit

.PHONY: test
test: pytest
