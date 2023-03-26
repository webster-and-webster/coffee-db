SOURCE_FOLDER = coffee_db

lint:
	flake8 $(SOURCE_FOLDER) --max-line-length 120
	black --check $(SOURCE_FOLDER)

test_app:
	pytest tests/test_coffee_db/.

test_integration:
	pytest tests/test_integration/.