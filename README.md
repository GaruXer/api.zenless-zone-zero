# Zenless Zone Zero API
This project is a RESTful API built with Python and FastAPI, focused on providing structured data for the game *Zenless Zone Zero* by HoYoverse. Since there is no official public API available, the data is collected through web scraping from two reliable community sources : the official [HoYoLab Wiki](https://wiki.hoyolab.com/pc/zzz/home) and [Honey Hunter World](https://zzz.honeyhunterworld.com). The API serves as a backend service that aggregates and exposes game-related information — such as agents, bangboo, w-engines and drives discs — to be easily consumed by frontends, tools, or analytics platforms.

## Installation Guide
Follow the steps below to set up and run the project locally.

### Prerequisites
Before getting started, make sure you have the following installed :

- [Python](https://www.python.org/) (version 3.13 or higher recommended)  
- [Docker](https://www.docker.com/) and Docker Compose  

### Configure Environment Variables

Create a `.env` file at the root of the project with the following content :

```.env
ENV=prod
API_VERSION=1.0.0
DATABASE_URL=postgresql://user:password@localhost:5432/database
```

### Create a Virtual Environment
Create a virtual environment to isolate project dependencies :
```bash
python -m venv .venv
```

### Activate the Virtual Environment
Depending on your operating system, run the appropriate command :
- Linux / macOS :
```bash
source .venv/bin/activate
```

- Windows Bash :
```bash
source .venv/Scripts/activate
```

### Install Python Dependencies
Install the required packages using `pip` :
```bash
pip install -r requirements.txt
```

### Install Playwright
Install browsers for Playwright :
```bash
playwright install
```

### Start the Database with Docker
Launch the database container in the background using Docker Compose :
```bash
docker compose up -d
```

### Apply Database Migrations
Create the database schema using Alembic migrations :
```bash
make alembic-migrate
```

> [!WARNING]
> If `make` is not available on your system, you can manually run :
> ```bash
> alembic upgrade head
> ```

### Launch the Scraping Process
To start the web scraping process :
```bash
make scraping
```

> [!WARNING]
> If `make` is not available on your system, you can manually run :
> ```bash
> python scraper.py
> ```

### Start the API Server
Run the API server using `make` :
```bash
make uvicorn-start-prod
```

> [!WARNING]
> If `make` is not available on your system, you can manually run :
> ```bash
> uvicorn src.main:app --host localhost --port 8000
> ```

You’re all set! The API should now be up and running on http://localhost:8000, and the scraping script will populate the database as needed.