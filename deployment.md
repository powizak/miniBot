# Deployment and CI/CD Instructions for miniBot

## Requirements
- Docker & Docker Compose
- Git

### Installation instructions for a clean system

**Docker & Docker Compose:**
- The easiest way is to install [Docker Desktop](https://docs.docker.com/desktop/), which includes Docker Engine, CLI, and Compose.
  - **Windows:** [Install guide](https://docs.docker.com/desktop/setup/install/windows-install/)
  - **Mac:** [Install guide](https://docs.docker.com/desktop/setup/install/mac-install/)
  - **Linux:** [Install guide](https://docs.docker.com/desktop/setup/install/linux/)
- On Linux, you can also install Compose as a plugin: [instructions](https://docs.docker.com/compose/install/linux/).

**Git:**
- **Windows:** Download and run the installer from [git-scm.com/download/win](https://git-scm.com/download/win)
- **Linux:** `sudo apt install git-all` (Debian/Ubuntu), `sudo dnf install git-all` (Fedora/RHEL)
- **macOS:** Run `git` in the terminal, or download the installer from [git-scm.com/download/mac](https://git-scm.com/download/mac)

## Environment Variables
Copy `.env.example` to `.env` and fill in:
- `PIONEX_API_KEY`, `PIONEX_API_SECRET`, `GEMINI_API_KEY`, `INFLUXDB_TOKEN`, `SECRET_KEY`
- `BACKEND_PORT`, `FRONTEND_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `INFLUXDB_ORG`, `INFLUXDB_BUCKET`
All other variables have sensible defaults.

## First Run

1. Clone the repository:
   ```
   git clone [repo address]
   cd miniBot
   ```

2. Prepare environment:
   ```
   cp .env.example .env
   # Edit .env as needed
   ```

3. Build and start all services:
   ```
   docker-compose up --build
   ```

4. Access:
   - Backend: `http://localhost:${BACKEND_PORT}`
   - Frontend: `http://localhost:${FRONTEND_PORT}`

## Services Overview

- **backend**: FastAPI app, runs on `${BACKEND_PORT}`
- **frontend**: React app (static build via Nginx), runs on `${FRONTEND_PORT}`
- **postgres**: PostgreSQL 15, persistent volume at `./db/postgres`
- **influxdb**: InfluxDB 2.7

## Management

- Stop all services:
  ```
  docker-compose down
  ```
- Restart backend or frontend:
  ```
  docker-compose restart backend
  docker-compose restart frontend
  ```
- View logs:
  ```
  docker-compose logs backend
  docker-compose logs frontend
  docker-compose logs postgres
  docker-compose logs influxdb
  ```

## Running Tests

- **Backend**:
  ```
  docker-compose exec backend pytest backend/tests/
  ```
- **Frontend**:
  ```
  docker-compose exec frontend npm test
  ```

## CI/CD Recommendations

- Validate `.env` before build.
- Run tests for backend and frontend on each commit.
- Use `docker-compose up --build --abort-on-container-exit --exit-code-from backend` for integration testing.
- Recommended pipeline steps:
  1. Checkout code
  2. Copy and fill `.env`
  3. Build containers
  4. Run backend and frontend tests
  5. Deploy with `docker-compose up -d`

## Troubleshooting

- Check service logs for errors.
- Ensure all environment variables are set.
- For database issues, verify volumes and credentials.
  docker-compose logs -f backend
  docker-compose logs -f frontend
  ```

## Aktualizace systému

1. Stáhněte nové změny z repozitáře:
   ```
   git pull
   ```

2. Restartujte služby:
   ```
   docker-compose up --build
   ```

## Testování

- Backend testy:
  ```
  docker-compose exec backend pytest ../backend/tests
  ```
- Frontend testy:
  ```
  docker-compose exec frontend npm test -- --watchAll=false
  ```

## CI/CD

- Automatizované buildy, testy a deploy zajišťuje GitHub Actions workflow v `.github/workflows/ci-cd.yml`.
- **Poznámka:** CI/CD workflow je univerzální a nevyžaduje ruční zásah – stačí mít správně vyplněné API klíče v .env souboru.