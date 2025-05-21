# ========== UVICORN ========== #
uvicorn-start-dev:
	uvicorn src.main:app --host localhost --port 8080 --reload

uvicorn-start-prod:
	uvicorn src.main:app --host localhost --port 8000

# ========== ALEMBIC ========== #
alembic-create-migration:
	alembic revision --autogenerate -m "$(message)"

alembic-migrate:
	alembic upgrade head

# ========== SCRAPING ========== #
scraping:
	python scraper.py