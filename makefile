install:
	sudo apt-get update
	sudo apt-get install uvicorn
	sudo apt-get install postgresql postgresql-contrib
	pip3 install -r requirements.txt

makemigrations:
	alembic revision -m "make migration file"

migrate:
	alembic update head
