FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

# Run tests if TEST=true is set (for CI/CD)
ARG TEST=false
RUN if [ "$TEST" = "true" ]; then pytest backend/tests/; fi

CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${BACKEND_PORT:-8000}"