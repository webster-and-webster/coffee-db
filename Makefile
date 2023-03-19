SOURCE_FOLDER = coffee_db

lint:
	flake8 $(SOURCE_FOLDER) --max-line-length 120
	black --check $(SOURCE_FOLDER)