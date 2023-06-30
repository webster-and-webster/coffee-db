SOURCE_FOLDER = coffee_db

lint:
	flake8 $(SOURCE_FOLDER) --max-line-length 120
	black --check $(SOURCE_FOLDER)

unit-tests:
	pytest tests/test_coffee_db/.

integration-tests:
	pytest tests/test_integration/.