format: style lint type

style:
	isort --atomic obp-api.py
	black obp-api.py

lint:
	flake8 obp-api.py
	autoflake --recursive obp-api.py

type:
	mypy --strict obp-api.py
