# ========== UVICORN ========== #
uvicorn-start:
	uvicorn src.main:app --host localhost --port 8080 --reload

# ========== ALEMBIC ========== #
alembic-create-migration:
	alembic revision --autogenerate -m "$(message)"

alembic-upgrade:
	alembic upgrade head

# ========== SCRAPING ========== #
scraping:
	python scraper.py