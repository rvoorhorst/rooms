install:
	pip3 install -r requirements.txt
	pip3 install -e .

migrate:
	python manage.py makemigrations
	python manage.py migrate

format:
	black --line-length 79 .
	isort .
