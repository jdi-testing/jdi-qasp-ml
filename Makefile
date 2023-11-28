.PHONY: clean
clean:
	@echo "Cleaning up ..."
	@find . -name \*.pyc -delete
	@find . -name \*.pyo -delete
	@find . -name \__pycache__ -exec rm -rf {} +

.PHONY: lint
lint:
	@echo "Linting ..."
	@flake8 Angular_model app BS_model ds_methods generators HTML5_model MUI_model tests utils vars

.PHONY: unittest
unittest: clean lint
	@echo "Unit tests ..."
	@pytest tests
